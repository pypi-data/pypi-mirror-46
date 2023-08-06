from datetime import datetime

from marshmallow import fields, Schema, post_load

from fasvaorm import Module, Aggregation, Configuration, Enrichment, Driver, Drive, Record, Measurement, Sensor, Signal, \
    Unit, Transferred, Valuetype, Vehicle, SignalsignalgroupMapping, RecordTransferredMapping, \
    ConfigurationSensorMapping


class SerializableDateTimeField(fields.DateTime):

    def _deserialize(self, value, attr, data):
        if isinstance(value, datetime):
            return value
        return super()._deserialize(value, attr, data)
    
    
class ModuleSchema(Schema):
    """
    Module marshal template
    """
    name = fields.String(required=True, allow_none=False)
    state = fields.String(required=True, allow_none=True, default=None)
    processing = fields.List(fields.String(), required=True, allow_none=True)
    processed = fields.List(fields.Dict(keys=fields.String()), required=True, allow_none=True)
    unprocessed = fields.List(fields.String(), required=True, allow_none=True)
    failed = fields.List(fields.String(), required=True, allow_none=True)

    @post_load
    def create(self, data):
        return Module(**data)


class AggregationSchema(Schema):
    timestamp = SerializableDateTimeField(format="iso", required=True, allow_none=False)
    iddrive = fields.Integer(required=True, allow_none=False)
    idaggregation = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Aggregation(**data)


class ConfigurationSchema(Schema):
    idvehicle = fields.Integer(required=True, allow_none=False)
    startDate = SerializableDateTimeField(format="iso",required=True, allow_none=False)
    idconfiguration = fields.Integer(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    endDate = SerializableDateTimeField(format="iso",required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Configuration(**data)


class ConfigurationSensorMappingSchema(Schema):
    idsensor = fields.Integer(required=True, allow_none=False)
    idconfiguration = fields.Integer(required=True, allow_none=False)
    idconfiguration_sensor = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return ConfigurationSensorMapping(**data)


class DriveSchema(Schema):
    end = SerializableDateTimeField(format="iso",required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    iddrive = fields.Integer(required=False, allow_none=True)
    idvehicle = fields.Integer(required=True, allow_none=False)
    start = SerializableDateTimeField(format="iso",required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Drive(**data)


class DriverSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    iddriver = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Driver(**data)


class EnrichmentSchema(Schema):
    idenrichment = fields.Integer(required=False, allow_none=True)
    enricher = fields.String(required=True, allow_none=False)
    idaggregation = fields.Integer(required=True, allow_none=False)
    enriched_on = SerializableDateTimeField(format="iso",required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Enrichment(**data)


class MeasurementSchema(Schema):
    textvalue = fields.String(required=False, allow_none=True)
    idmeasurement = fields.Integer(required=False, allow_none=True)
    binaryvalue = fields.Raw(required=False, allow_none=True)
    idrecord = fields.Integer(required=False, allow_none=True)
    timestamp = SerializableDateTimeField(format="iso",required=True, allow_none=False)
    idvehicle = fields.Integer(required=True, allow_none=False)
    doublevalue = fields.Decimal(required=False, allow_none=True)
    idsignal = fields.Integer(required=True, allow_none=False)
    flagvalue = fields.Boolean(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Measurement(**data)


class RecordSchema(Schema):
    drive_length = fields.Decimal(required=True, allow_none=False)
    start_mileage = fields.Decimal(required=True, allow_none=False)
    iddrive = fields.Integer(required=False, allow_none=True)
    start_time = SerializableDateTimeField(format="iso",required=True, allow_none=False)
    idrecord = fields.Integer(required=False, allow_none=True)
    end_mileage = fields.Decimal(required=True, allow_none=False)
    filepath = fields.String(required=True, allow_none=False)
    iddriver = fields.Integer(required=True, allow_none=False)
    end_time = SerializableDateTimeField(format="iso",required=True, allow_none=False)
    idvehicle = fields.Integer(required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Record(**data)


class RecordTransferredMappingSchema(Schema):
    idtransferred = fields.Integer(required=True, allow_none=False)
    idrecord_transferred = fields.Integer(required=False, allow_none=True)
    idrecord = fields.Integer(required=True, allow_none=False)

    @post_load
    def create(self, data):
        return RecordTransferredMapping(**data)


class SensorSchema(Schema):
    idsensor = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=True, allow_none=False)
    additional_informations = fields.Raw(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    parameter = fields.String(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Sensor(**data)


class SignalSchema(Schema):
    idsensor = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)
    idvaluetype = fields.Integer(required=True, allow_none=False)
    idsignal = fields.Integer(required=False, allow_none=True)
    idunit = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Signal(**data)


class SignalsignalgroupMappingSchema(Schema):
    idsignalgroup = fields.Integer(required=True, allow_none=False)
    idsignal = fields.Integer(required=True, allow_none=False)
    idsignal_signalgroup_mapping = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return SignalsignalgroupMapping(**data)


class TransferredSchema(Schema):
    idtransferred = fields.Integer(required=False, allow_none=True)
    directory = fields.String(required=True, allow_none=False)
    date = SerializableDateTimeField(format="iso",required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Transferred(**data)


class UnitSchema(Schema):
    idunit = fields.Integer(required=True, allow_none=False)
    name = fields.String(required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Unit(**data)


class ValuetypeSchema(Schema):
    name = fields.String(required=True, allow_none=False)
    idvaluetype = fields.Integer(required=False, allow_none=True)

    @post_load
    def create(self, data):
        return Valuetype(**data)


class VehicleSchema(Schema):
    dimension_width = fields.Integer(required=True, allow_none=False)
    dimension_height = fields.Integer(required=True, allow_none=False)
    serial_number = fields.String(required=True, allow_none=False)
    idvehicle = fields.Integer(required=False, allow_none=True)
    description = fields.String(required=False, allow_none=True)
    dimension_length = fields.Integer(required=True, allow_none=False)

    @post_load
    def create(self, data):
        return Vehicle(**data)
