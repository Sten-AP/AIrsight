import { Card, Title, Table, TableHead, TableRow, TableHeaderCell, TableBody, TableCell, Subtitle } from "@tremor/react";

export default function Information() {
  return (
    <>
    <Subtitle className='mt-5 mb-2'>Description of table contents</Subtitle>
      <Card>
        <Table>
          <TableHead>
            <TableRow>
              <TableHeaderCell>Column</TableHeaderCell>
              <TableHeaderCell>Description</TableHeaderCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell>Type</TableCell>
              <TableCell>The type of measurement - Sensor, Satellite, or Prediction.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Timestamp (UTC)</TableCell>
              <TableCell>The timestamp of the measurement in Coordinated Universal Time (UTC).</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Country</TableCell>
              <TableCell>The country where the measurement was taken.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Region</TableCell>
              <TableCell>The specific region within the country where the measurement was taken.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>NO2 (µg/m³)</TableCell>
              <TableCell>The concentration of Nitrogen Dioxide in micrograms per cubic meter.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>PM 25 (µg/m³)</TableCell>
              <TableCell>The concentration of Particulate Matter (PM2.5) in micrograms per cubic meter.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>PM 10 (µg/m³)</TableCell>
              <TableCell>The concentration of Particulate Matter (PM10) in micrograms per cubic meter.</TableCell>
            </TableRow>
            <TableRow>
              <TableCell>Quality</TableCell>
              <TableCell>The air quality categorized based on PM10 concentration.</TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </Card>
      <Subtitle className='mt-5 mb-2'>Exporting data</Subtitle>
       When you click the 'Download CSV' button, it exports a dataset tailored to the filters you've applied. The exported measurements retain all decimal values for precision, even though they are displayed with fixed decimals set to two on the interface. This ensures that you get the most accurate and detailed air quality data in the exported CSV file.
    </>
  );
}
