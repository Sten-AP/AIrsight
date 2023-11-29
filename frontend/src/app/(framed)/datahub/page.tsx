"use client";
import {
  Card,
  Grid,
  Text,
  Title
} from "@tremor/react";
import TableDataHub from "./components/tableDataHub";
import TableHeadActions from "./components/tableHeadActions";

export default function Page() {
  return (
    <>
      <Title>DataHub</Title>
      <Text>An interactive hub that can provide the airquality data AIrsight collected from sensors and satellites, it also provides predictions using AI.</Text>

      {/* Main section */}
      <Card className='mt-6'>
        <TableHeadActions />
        <TableDataHub />
      </Card>

      {/* KPI section */}
      <Grid numItemsMd={2} className='mt-6 gap-6'>
        <Card>
          {/* Placeholder to set height */}
          <div className='h-28' />
        </Card>
        <Card>
          {/* Placeholder to set height */}
          <div className='h-28' />
        </Card>
      </Grid>
    </>
  );
}
