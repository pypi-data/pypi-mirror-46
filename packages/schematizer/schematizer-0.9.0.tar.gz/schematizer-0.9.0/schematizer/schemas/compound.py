from dataclasses import make_dataclass
from schematizer.exceptions import (
    BaseValidationError, CompoundValidationError, NestedValidationError, SimpleValidationError, StopValidation,
)
from schematizer.key import Key
from schematizer.schemas.base import BaseCoercibleSchema, BaseSchema


def _force_key(str_or_key):
    if isinstance(str_or_key, Key):
        return str_or_key
    else:
        return Key(str_or_key)


class List(BaseCoercibleSchema):
    coerce_primitive = list

    def __init__(self, schema):
        super().__init__()
        self.schema = schema

    def to_native(self, obj):
        obj = super().to_native(obj)
        result = []
        errors = []
        for i, item in enumerate(obj):
            try:
                result.append(self.schema.to_native(item))
            except BaseValidationError as exc:
                errors.append(NestedValidationError(i, exc))
        if errors:
            raise CompoundValidationError(errors)
        else:
            return result

    def to_primitive(self, obj):
        return [self.schema.to_primitive(item) for item in obj]


class BaseEntity(BaseCoercibleSchema):
    coerce_primitive = dict

    def __init__(self, *args, **kwargs):
        super().__init__()
        try:
            schemas, = args
            assert not kwargs, 'No keyword arguments allowed'
        except ValueError:
            schemas = kwargs
            assert not args, 'No positional arguments allowed'
        self.schemas = {
            _force_key(str_or_key): schema
            for str_or_key, schema in schemas.items()
        }

    def __call__(self, *args, **kwargs):
        native_type = self.get_native_type()
        return native_type(*args, **kwargs)

    def get_native_type(self):
        raise NotImplementedError

    def get_native_accessor(self):
        raise NotImplementedError

    def get_native_accessor_error(self):
        raise NotImplementedError

    def extended(self, *args, **kwargs):
        extension_schema = self.__class__(*args, **kwargs)
        return self.__class__({**self.schemas, **extension_schema.schemas})

    def to_native(self, obj):
        obj = super().to_native(obj)
        result = {}
        errors = []
        for key, schema in self.schemas.items():
            try:
                value = obj[key.primitive]
            except KeyError:
                if key.is_required:
                    error = NestedValidationError(
                        key.primitive, SimpleValidationError('MISSING'),
                    )
                    errors.append(error)
                continue
            try:
                result[key.native] = schema.to_native(value)
            except BaseValidationError as exc:
                errors.append(
                    NestedValidationError(key.primitive, exc),
                )
        if errors:
            raise CompoundValidationError(errors)
        else:
            return self(**result)

    def to_primitive(self, obj):
        result = {}
        native_accessor = self.get_native_accessor()
        native_accessor_error = self.get_native_accessor_error()
        for key, schema in self.schemas.items():
            try:
                value = native_accessor(obj, key.native)
            except native_accessor_error:
                if key.is_required:
                    raise
                else:
                    continue
            result[key.primitive] = schema.to_primitive(value)
        return result


class Dict(BaseEntity):
    def get_native_type(self):
        return dict

    def get_native_accessor(self):
        return dict.__getitem__

    def get_native_accessor_error(self):
        return KeyError


class DataClass(BaseEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.native_type = make_dataclass('DataClass', [key.native for key in self.schemas], frozen=True)

    def get_native_type(self):
        return self.native_type

    def get_native_accessor(self):
        return getattr

    def get_native_accessor_error(self):
        return AttributeError


class Called(BaseSchema):
    def __init__(self, schema, *args, **kwargs):
        self.schema = schema
        self.args = args
        self.kwargs = kwargs

    def to_native(self, obj):
        return self.schema.to_native(obj)

    def to_primitive(self, obj):
        return self.schema.to_primitive(
            obj(*self.args, **self.kwargs),
        )


class Wrapped(BaseSchema):
    def __init__(self, schema, validators):
        super().__init__()
        self.schema = schema
        self.validators = validators

    def to_native(self, obj):
        try:
            for validator in self.validators:
                validator.validate_primitive(obj)
        except StopValidation:
            return obj
        obj = self.schema.to_native(obj)
        for validator in self.validators:
            validator.validate_native(obj)
        return obj

    def to_primitive(self, obj):
        try:
            for validator in self.validators:
                validator.validate_native(obj)
        except StopValidation:
            return obj
        obj = self.schema.to_primitive(obj)
        for validator in self.validators:
            validator.validate_primitive(obj)
        return obj
