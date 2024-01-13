"use client";
import { Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Badge, BadgeDelta, Card, Text, Button } from "@tremor/react";
import { getPredictionData, getSatelliteData, getSensorData } from "@/src/utils/apiUtils";
import { Dispatch, SetStateAction, useEffect, useState } from "react";
import { AirQualityMeasurement } from "@/src/types/AirsightTypes";
import { differenceInDays, format, formatDistance } from "date-fns";
import { CSVLink } from "react-csv";

export default function TableDataHub({selectedIndex, startDate, endDate, measurementData, setMeasurementData} : {selectedIndex : number, startDate: Date, endDate: Date, measurementData: AirQualityMeasurement[] | null, setMeasurementData: Dispatch<SetStateAction<AirQualityMeasurement[] | null>>}) {
   
  useEffect(() => {
    async function fetchData() {
      try {
        const resSensor = await getSensorData(startDate, endDate);
        const resSat = await getSatelliteData(startDate, endDate);
        const resPred = await getPredictionData(startDate, endDate);

        let newData: any[] = [];

        if (resSensor) {
          newData = [...newData, ...resSensor];
        }
        if (resSat) {
          newData = [...newData, ...resSat];
        }
        if (resPred) {
          newData = [...newData, ...resPred];
        }

        setMeasurementData(newData);
      } catch (error) {
        console.error(error);
        setMeasurementData(null);
      }
    }
    fetchData()
  }, [startDate, endDate]);

  return (
    <>
        <Table className='mt-6'>
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
            {measurementData != null && measurementData.length > 0 ? (
              measurementData.filter(m => {
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
                    <TableCell className='text-right'>Belgium</TableCell>
                    <TableCell className='text-right'>Antwerp</TableCell>
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
                <TableCell>{measurementData != null ? <Badge color='blue'>Loading...</Badge> : <Badge color='red'>Try again later</Badge>}</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
    </>
  );
}

