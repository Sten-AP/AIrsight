const axios = require('axios');

async function getAllWekeoSensorMeasurements(start_date: Date, stop_date: Date) {
  try {
    const data = {
      start_date: start_date.toUTCString(),
      stop_date: stop_date.toUTCString(),
    };

    const response = await axios.get('https://airsight.cloudsin.space/api/wekeo/', {
      method: 'get',
      maxBodyLength: Infinity,
      headers: {
        'Content-Type': 'application/json',
      },
      params: data,
    });

    return response.data;
  } catch (error) {
    console.error(error);
    throw error; // You may want to handle the error differently based on your use case
  }
}
