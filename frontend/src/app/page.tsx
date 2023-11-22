import Image from "next/image";
import { Card, Grid, Title, Text, Tab, TabList, TabGroup, TabPanel, TabPanels } from "@tremor/react";

export default function Page() {
 return (
  <main className="p-4 md:p-10 mx-auto max-w-7xl">
   <Title>Dashboard</Title>
   <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr.</Text>
   <TabGroup className="mt-6">
    <TabList>
     <Tab>Page 1</Tab>
     <Tab>Page 2</Tab>
    </TabList>
    <TabPanels>
     <TabPanel>
      <Grid numItemsMd={2} numItemsLg={3} className="gap-6 mt-6">
       <Card>
        {/* Placeholder to set height */}
        {/* <div className="h-28" /> */}
        <iframe src="https://airsight.cloudsin.space/grafana/d-solo/bb08a297-a2d9-458a-9d7c-06258271aec3/airsight?orgId=1&theme=light&panelId=2&refresh=10min" width="100%" height="200px"></iframe>
       </Card>
       <Card>
        {/* Placeholder to set height */}
        {/* <div className="h-28" /> */}
        <iframe src="https://airsight.cloudsin.space/grafana/d-solo/bb08a297-a2d9-458a-9d7c-06258271aec3/airsight?orgId=1&theme=light&panelId=3&refresh=10min" width="100%" height="200px"></iframe>
       </Card>
       <Card>
        {/* Placeholder to set height */}
        {/* <div className="h-28" /> */}
        <iframe src="https://airsight.cloudsin.space/grafana/d-solo/bb08a297-a2d9-458a-9d7c-06258271aec3/airsight?orgId=1&theme=light&panelId=4&refresh=10min" width="100%" height="200px"></iframe>
       </Card>
      </Grid>
      <div className="mt-6">
       <Card>
        {/* Placeholder to set height */}
        {/* <div className="h-80" /> */}
        <iframe src="https://airsight.cloudsin.space/grafana/d-solo/bb08a297-a2d9-458a-9d7c-06258271aec3/airsight?orgId=1&theme=light&panelId=1&refresh=60min" width="100%" height="200px"></iframe>
       </Card>
      </div>
     </TabPanel>
     <TabPanel>
      <div className="mt-6">
       <Card>
        <div className="h-96" />
       </Card>
      </div>
     </TabPanel>
    </TabPanels>
   </TabGroup>
  </main>
 );
}
