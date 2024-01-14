import axios from "axios";
import { Country, AirQualityMeasurement, serializeWekeoData, WekeoSensorMeasurement, Measurement, serializeMeasurement, MeasurementType } from "../types/AirsightTypes";
import { format } from "date-fns";

function formatDateToString(date: Date): string {
  return `${format(date, 'yyyy-MM-dd')}T00:00:00`
}
export async function getSensorData(startDate: Date, endDate: Date): Promise<AirQualityMeasurement[] | null> {
  try {
    const data = {
      start_date: formatDateToString(startDate),
      stop_date: formatDateToString(endDate),
    };

    const response = await axios.get("https://airsight.cloudsin.space/api/openaq/", {
      headers: {
        "Content-Type": "application/json",
      },
      params: data,
    });
    
    let result: AirQualityMeasurement[] = [];

    response.data.forEach((e: Measurement) => {
      result.push(serializeMeasurement(e, MeasurementType.Sensor));
    });

    return result;

  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getSatelliteData(startDate: Date, endDate: Date): Promise<AirQualityMeasurement[] | null> {
  try {
    const data = {
      start_date: formatDateToString(startDate),
      stop_date: formatDateToString(endDate),
    };

    const response = await axios.get("https://airsight.cloudsin.space/api/wekeo/", {
      headers: {
        "Content-Type": "application/json",
      },
      params: data,
    });

    let result: AirQualityMeasurement[] = [];

    response.data.forEach((e: WekeoSensorMeasurement) => {
      result.push(serializeWekeoData(e));
    });

    return result;

  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getPredictionData(startDate: Date, endDate: Date): Promise<AirQualityMeasurement[] | null> {
  try {
    const data = {
      start_date: formatDateToString(startDate),
      stop_date: formatDateToString(endDate),
    };

    const response = await axios.get("https://airsight.cloudsin.space/api/predictions/", {
      headers: {
        "Content-Type": "application/json",
      },
      params: data,
    });

    let result: AirQualityMeasurement[] = [];

    response.data.forEach((e: Measurement) => {
      result.push(serializeMeasurement(e, MeasurementType.Prediction));
    });

    return result;

  } catch (error) {
    console.error(error);
    return null;
  }
}

export async function getLocations(): Promise<Country[] | null> {
  try {
    const response = await axios.get("https://airsight.cloudsin.space/api/locations/", {
      headers: {
        "Content-Type": "application/json",
      },
    });

    return response.data;
  } catch (error) {
    console.error(error);
    return null;
  }
}