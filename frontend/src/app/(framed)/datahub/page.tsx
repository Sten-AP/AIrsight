"use client";
import { Button, Card, Text, Title, Dialog, DialogPanel } from "@tremor/react";
import TableDataHub from "./components/tableDataHub";
import TableHeadActions from "./components/tableHeadActions";
import { getLocations } from "@/src/utils/apiUtils";
import { useState, useEffect, SetStateAction } from "react";
import { AirQualityMeasurement, Country } from "@/src/types/AirsightTypes";
import Information from "./components/information";
import { sub } from "date-fns";

export default function Page() {
  const [locations, setLocations] = useState<Country[] | null>(null);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [isOpen, setIsOpen] = useState(false);
  const [startDate, setStartDate] = useState<Date>(new Date(Date.now()));
  const [endDate, setEndDate] = useState<Date>(new Date(Date.now()));
  const [measurementData, setMeasurementData] = useState<AirQualityMeasurement[] | null>([]);

  useEffect(() => {
    async function fetchLocations() {
      try {
        const result = await getLocations();
        setLocations(result);
      } catch (error) {
        console.error(error);
        setLocations(null);
      }
    }
    fetchLocations();
  }, []);

  return (
    <>
      <Title>DataHub</Title>
      <Text>An interactive hub that can provide the airquality data AIrsight collected from sensors and satellites, it also provides predictions using AI.</Text>
      <Button className="mt-2" onClick={() => setIsOpen(true)}>Show documentation</Button>
      <Card className='mt-6'>
        {locations ? (
          <>
            <TableHeadActions locations={locations} setSelectedIndex={setSelectedIndex} selectedIndex={selectedIndex} startDate={startDate} setStartDate={setStartDate} endDate={endDate} setEndDate={setEndDate} measurementData={measurementData} />
            <TableDataHub selectedIndex={selectedIndex} startDate={startDate} endDate={endDate} measurementData={measurementData} setMeasurementData={setMeasurementData} />
          </>
        ) : (
          <Text>Getting everything ready</Text>
        )}
      </Card>
      <Dialog className="w-full" open={isOpen} onClose={(val) => setIsOpen(val)} static={true}>
        <DialogPanel>
          <Title className='mb-3'>DataHub documentation</Title>
          <Information />
          <div className='mt-3'>
            <Button variant='light' onClick={() => setIsOpen(false)}>
              Got it!
            </Button>
          </div>
        </DialogPanel>
      </Dialog>
    </>
  );
}
