"use client";
import { ArrowDownTrayIcon } from "@heroicons/react/24/outline";
import { MultiSelect, MultiSelectItem, DateRangePicker, Button, TabGroup, TabList, Tab, SelectItem, Select } from "@tremor/react";
import { Dispatch, SetStateAction, useState } from "react";
import airqualityData from "../dummyData.json";
import { AirQualityMeasurement, Country } from "@/src/types/AirsightTypes";
import { CSVLink } from "react-csv";

export default function TableHeadActions({
  locations,
  selectedIndex,
  setSelectedIndex,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  measurementData,
}: {
  locations: Country[];
  selectedIndex: number;
  setSelectedIndex: Dispatch<SetStateAction<number>>;
  startDate: Date;
  setStartDate: Dispatch<SetStateAction<Date>>;
  endDate: Date;
  setEndDate: Dispatch<SetStateAction<Date>>;
  measurementData: AirQualityMeasurement[] | null;
}) {
  const getQualityLabel = (pm10: any) => {
    if (pm10 > 20) {
      return "Fair";
    } else if (pm10 > 40) {
      return "Moderate";
    } else {
      return "Good";
    }
  };

  const csvData = [
    ["ID", "Timestamp", "Country", "Region", "NO2 (µg/m³)", "PM 25 (µg/m³)", "PM 10 (µg/m³)", "Quality"],
    ...(measurementData || []).map((item) => [
      item.id,
      item.time.toISOString(),
      "Belgium",
      "Antwerp",
      item.no2 ? item.no2 : "null",
      item.pm25 ? item.pm25 : "null",
      item.pm10 ? item.pm10 : "null",
      getQualityLabel(item.pm10),
    ]),
  ];

  const [selectedRegion, setRegion] = useState([]);
  const [country, setCountry] = useState("BE");
  return (
    <div className='md:flex justify-between'>
      <div className='flex gap-2 space-x-2'>
        <Select placeholder='Belgium' className='max-w-xs w-12' defaultValue='BE' onValueChange={setCountry}>
          {locations.map((l) => (
            <SelectItem key={l.code} value={l.code}>
              {l.country}
            </SelectItem>
          ))}
        </Select>
        <MultiSelect placeholder='Region' className='max-w-xs w-56'>
          {locations.filter((l) => l.code == country)[0] != undefined
            ? locations
                .filter((l) => l.code == country)[0]
                .regions.map((item) => (
                  <MultiSelectItem key={item} value={item}>
                    {item}
                  </MultiSelectItem>
                ))
            : locations
                .filter((l) => l.code == "BE")[0]
                .regions.map((item) => (
                  <MultiSelectItem key={item} value={item}>
                    {item}
                  </MultiSelectItem>
                ))}
        </MultiSelect>
        <DateRangePicker
          className='max-w-md mx-auto w-fit'
          defaultValue={{ from: startDate, to: endDate }}
          onValueChange={(v) => {
            if (v.from && v.to) {
              console.warn(v);
              setStartDate(v.from);
              setEndDate(v.to);
            }
          }}
          enableSelect={false}
        />
        <CSVLink data={csvData} filename='airsight_measurement_data.csv'>
          <Button color='gray' icon={ArrowDownTrayIcon}>
            Download CSV
          </Button>
        </CSVLink>
      </div>
      <div>
        <TabGroup index={selectedIndex} onIndexChange={setSelectedIndex}>
          <TabList color='gray' variant='solid'>
            <Tab>All</Tab>
            <Tab>Sensors</Tab>
            <Tab>Satellites</Tab>
            <Tab>Predictions</Tab>
          </TabList>
        </TabGroup>
      </div>
    </div>
  );
}
