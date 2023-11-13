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
                <iframe src="http://airsight.westeurope.cloudapp.azure.com:3002/d-solo/bfccfc6b-761e-4c71-a9ff-e79912e7e7e3/airsight?orgId=2&theme=light&panelId=1&refresh=30min" width="100%" height="200px"></iframe>
              </Card>
              <Card>
                {/* Placeholder to set height */}
                {/* <div className="h-28" /> */}
                <iframe src="http://airsight.westeurope.cloudapp.azure.com:3002/d-solo/bfccfc6b-761e-4c71-a9ff-e79912e7e7e3/airsight?orgId=2&theme=light&panelId=2&refresh=30min" width="100%" height="200px"></iframe>
              </Card>
              <Card>
                {/* Placeholder to set height */}
                {/* <div className="h-28" /> */}
                <iframe src="http://airsight.westeurope.cloudapp.azure.com:3002/d-solo/bfccfc6b-761e-4c71-a9ff-e79912e7e7e3/airsight?orgId=2&theme=light&panelId=3&refresh=30min" width="100%" height="200px"></iframe>
              </Card>
            </Grid>
            <div className="mt-6">
              <Card>
                {/* Placeholder to set height */}
                {/* <div className="h-80" /> */}
                <iframe src="http://airsight.westeurope.cloudapp.azure.com:3002/d-solo/bfccfc6b-761e-4c71-a9ff-e79912e7e7e3/airsight?orgId=2&theme=light&panelId=4" width="100%" height="400px"></iframe>
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
