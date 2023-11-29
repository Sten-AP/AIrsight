import { Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Badge, BadgeDelta } from "@tremor/react";
import airqualityData from "../dummyData.json";

export default async function TableDataHub() {
  return (
  <>
    <Table className='mt-6'>
      <TableHead>
        <TableRow>
          <TableHeaderCell>Type</TableHeaderCell>
          <TableHeaderCell>Timestamp</TableHeaderCell>
          <TableHeaderCell className='text-right'>Country</TableHeaderCell>
          <TableHeaderCell className='text-right'>Region</TableHeaderCell>
          <TableHeaderCell className='text-right'>PM 2.5 (µg/m³)</TableHeaderCell>
          <TableHeaderCell className='text-right'>PM 5 (µg/m³)</TableHeaderCell>
          <TableHeaderCell className='text-right'>PM 10 (µg/m³)</TableHeaderCell>
          <TableHeaderCell className='text-right'>Quality</TableHeaderCell>
        </TableRow>
      </TableHead>

      <TableBody>
        {airqualityData.map((item) => (
          <TableRow key={item.timestamp}>
            <TableCell>
              <Badge color='slate'>{item.measurementType}</Badge>
            </TableCell>
            <TableCell>{item.timestamp}</TableCell>
            <TableCell className='text-right'>{item.country}</TableCell>
            <TableCell className='text-right'>{item.region}</TableCell>
            <TableCell className='text-right'>{item.pm25}</TableCell>
            <TableCell className='text-right'>{item.pm5}</TableCell>
            <TableCell className='text-right'>{item.pm10}</TableCell>
            <TableCell className='text-right'>
              <BadgeDelta deltaType={item.deltaType} size='xs'>
                {item.status}
              </BadgeDelta>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </>);
}
