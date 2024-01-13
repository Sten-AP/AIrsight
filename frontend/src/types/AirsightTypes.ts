export interface Country {
  country: string;
  code: string;
  regions: string[];
}

export interface AirQualityMeasurement {
  id: string;
  time: Date;
  lat: number;
  lon: number;
  no2: number;
  o3: number;
  pm10: number;
  pm25: number;
  so2: number;
  type: MeasurementType;
}

export interface Measurement {
  id: string;
  time: Date;
  lat: number;
  lon: number;
  no2: number;
  o3: number;
  pm10: number;
  pm25: number;
  so2: number;
  type: MeasurementType;
}

export interface WekeoSensorMeasurement {
  id: string;
  time: string;
  co_conc: number;
  lat: number;
  lon: number;
  no2_conc: number;
  o3_conc: number;
  pm10_conc: number;
  pm2p5_conc: number;
  so2_conc: number;
}

export function serializeMeasurement(data: Measurement, measurementType: MeasurementType): AirQualityMeasurement {
  return {
    id: data.id,
    time: new Date(data.time),
    lat: data.lat,
    lon: data.lon,
    no2: data.no2,
    o3: data.o3,
    pm10: data.pm10,
    pm25: data.pm25,
    so2: data.so2,
    type: measurementType,
  };
}

export function serializeWekeoData(data: WekeoSensorMeasurement): AirQualityMeasurement {
  return {
    id: data.id,
    time: new Date(data.time),
    lat: data.lat,
    lon: data.lon,
    no2: data.no2_conc,
    o3: data.o3_conc,
    pm10: data.pm10_conc,
    pm25: data.pm2p5_conc,
    so2: data.so2_conc,
    type: MeasurementType.Satellite,
  };
}

export enum MeasurementType {
  Sensor,
  Satellite,
  Prediction,
}