import { ArrowDownTrayIcon } from "@heroicons/react/24/outline";
import { MultiSelect, MultiSelectItem, DateRangePicker, Button, TabGroup, TabList, Tab } from "@tremor/react";
import { useState } from "react";
import airqualityData from "../dummyData.json";

export default function TableHeadActions() {
    const [selectedRegion, setRegion] = useState([]);
    const [selectedIndex, setSelectedIndex] = useState(0);
    return (
        <div className='md:flex justify-between'>
          <div className='flex gap-2 space-x-2'>
            <MultiSelect placeholder='Country' className='max-w-xs'>
              <MultiSelectItem key={"1"} value={"BE"}>
                BE
              </MultiSelectItem>
            </MultiSelect>
            <MultiSelect placeholder='Region' className='max-w-xs'>
              {airqualityData.map((item) => (
                <MultiSelectItem key={item.region} value={item.region}>
                  {item.region}
                </MultiSelectItem>
              ))}
            </MultiSelect>
            <DateRangePicker className="max-w-xs mx-auto" enableSelect={false} />
            <Button color="gray" icon={ArrowDownTrayIcon}>Download CSV</Button>
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