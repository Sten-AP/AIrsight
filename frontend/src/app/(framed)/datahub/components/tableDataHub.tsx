"use client";
import { Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Badge, BadgeDelta, Card, Text, Button } from "@tremor/react";
import { getPredictionData, getSatelliteData, getSensorData } from "@/src/utils/apiUtils";
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import { AirQualityMeasurement } from "@/src/types/AirsightTypes";
import { differenceInDays, format, formatDistance } from "date-fns";
var numeral = require('numeral');

export default function TableDataHub({selectedIndex, startDate, endDate, measurementData, setMeasurementData} : {selectedIndex : number, startDate: Date, endDate: Date, measurementData: AirQualityMeasurement[] | null, setMeasurementData: Dispatch<SetStateAction<AirQualityMeasurement[] | null>>}) {
  const [iterMeasurementData, setIterMeasurementData] = useState<AirQualityMeasurement[] | null>([]);
  let timer: NodeJS.Timeout;

  useEffect(() => {
    async function fetchData() {
      try {
        const resSensor = await getSensorData(startDate, endDate);
        const resSat = await getSatelliteData(startDate, endDate);
        const resPred = await getPredictionData(startDate, endDate);

        let newData: any[] = [];
        let iterData: any[] = [];

        if (resSensor) {
          newData = [...newData, ...resSensor];
          iterData = [...iterData, ...resSensor.slice(0, 200)];
        }
        if (resSat) {
          newData = [...newData, ...resSat];
          iterData = [...iterData, ...resSat.slice(0, 200)];
        }
        if (resPred) {
          newData = [...newData, ...resPred];
          iterData = [...iterData, ...resPred.slice(0, 200)];
        }
        setMeasurementData([]);
        setIterMeasurementData([]);
        setMeasurementData(newData);
        setIterMeasurementData(iterData);
      } catch (error) {
        console.error(error);
        setMeasurementData(null);
      }
    }

    timer = setTimeout(() => {
      fetchData();
    }, 2000);
    
    return () => clearTimeout(timer);

  }, [startDate, endDate]);

  let displayedRows = 0;
  let totalRows;

  if(iterMeasurementData != null && measurementData != null && iterMeasurementData.length > 0 && measurementData.length > 0) {
    displayedRows = iterMeasurementData.filter(m => {
      if(selectedIndex != 0) {
        return m.type.valueOf() == selectedIndex - 1
      } else {
        return true
      }
    }).length;

    totalRows = measurementData.filter(m => {
      if(selectedIndex != 0) {
        return m.type.valueOf() == selectedIndex - 1
      } else {
        return true
      }
    }).length;
  }

  return (
    <>
    <Text className="mt-6 px-4">
      {`${numeral(displayedRows).format('0,0')} of ${numeral(totalRows).format('0,0')} rows`}
    </Text>
        <Table className='mt-1'>
          <TableHead>
            <TableRow>
              <TableHeaderCell>Type</TableHeaderCell>
              <TableHeaderCell>Timestamp {"(UTC)"}</TableHeaderCell>
              <TableHeaderCell className='text-right'>Country</TableHeaderCell>
              <TableHeaderCell className='text-right'>Region</TableHeaderCell>
              <TableHeaderCell className='text-right'>NO2 (µg/m³)</TableHeaderCell>
              <TableHeaderCell className='text-right'>PM 25 (µg/m³)</TableHeaderCell>
              <TableHeaderCell className='text-right'>PM 10 (µg/m³)</TableHeaderCell>
              <TableHeaderCell className='text-right'>Quality</TableHeaderCell>
            </TableRow>
          </TableHead>

          <TableBody>
            {iterMeasurementData != null && iterMeasurementData.length > 0 ? (
              iterMeasurementData.filter(m => {
                if(selectedIndex != 0) {
                  return m.type.valueOf() == selectedIndex - 1
                } else {
                  return true
                }
              }).map((item, index) => {
                let deltaType = "increase";
                let qualityLabel = "Good";
                if (item.pm10 > 20) {
                  deltaType = "unchanged";
                  qualityLabel = "Fair";
                  if (item.pm10 > 40) {
                    deltaType = "decrease";
                    qualityLabel = "Moderate";
                  }
                }
                const date = new Date(item.time);
                return (
                  <TableRow key={item.pm10 + item.id + index}>
                    <TableCell>
                      <Badge color='slate'>{item.type == 0 ? 'Sensor' : item.type == 1 ? 'Satellite' : 'Prediction'}</Badge>
                    </TableCell>
                    <TableCell>
                      {differenceInDays(new Date(), date) <= 3 ? formatDistance(date, new Date(), { addSuffix: true }) : format(date, 'dd-MM-yyyy hh:mm')}
                    </TableCell>
                    <TableCell className='text-right'>{item.country ? item.country : "N/A"}</TableCell>
                    <TableCell className='text-right'>{item.region ? item.region : "N/A"}</TableCell>
                    <TableCell className='text-right'>{item.no2 ? item.no2.toFixed(2) : "N/A"}</TableCell>
                    <TableCell className='text-right'>{item.pm25 ? item.pm25.toFixed(2) : "N/A"}</TableCell>
                    <TableCell className='text-right'>{item.pm10 ? item.pm10.toFixed(2) : "N/A"}</TableCell>
                    <TableCell className='text-right'>
                      <BadgeDelta deltaType={deltaType} size='xs'>
                        {qualityLabel}
                      </BadgeDelta>
                    </TableCell>
                  </TableRow>
                );
              })
            ) : (
              <TableRow>
                <TableCell>{iterMeasurementData != null ? <Badge color='blue'>Loading...</Badge> : <Badge color='red'>Try again later</Badge>}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
    </>
  );
}

