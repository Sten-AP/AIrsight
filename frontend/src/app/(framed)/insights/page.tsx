import { Card, Grid, Tab, TabGroup, TabList, TabPanel, TabPanels, Text, Title } from "@tremor/react";
import GrafanaFrame from "../../components/grafanaFrame";

export default function Page() {
  return (
    <>
      <Title>Insights</Title>
      <Text>Several visualisations of the airquality data sourced from WeKeo, OpenAQ and AIrsight predictions.</Text>
      <Text>The green area indicates safe leves, the yellow area indicates a health risk to compromised groups, the red area indicates a health risk to all groups.</Text>
      <TabGroup className='mt-6'>
        <TabList>
          <Tab>Insights 1</Tab>
          <Tab>Insights 2</Tab>
        </TabList>
        <TabPanels>
          <TabPanel>
            <Grid numItemsMd={2} numItemsLg={3} className='gap-6 mt-6'>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={7} refreshRate={600} className={"w-full h-full rounded-tremor-default"} timeFrame="48h"/>
              </Card>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={8} refreshRate={600} className={"w-full h-full rounded-tremor-default"} timeFrame="48h"/>
              </Card>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={11} refreshRate={600} className={"w-full h-full rounded-tremor-default"} timeFrame="48h"/>
              </Card>
            </Grid>
          </TabPanel>
          <TabPanel>
            <Grid numItemsMd={2} numItemsLg={3} className='gap-6 mt-6'>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={2} refreshRate={600} className={"w-full h-full rounded-tremor-default"}/>
              </Card>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={3} refreshRate={600} className={"w-full h-full rounded-tremor-default"}/>
              </Card>
              <Card className="p-0 h-80">
                <GrafanaFrame panelId={4} refreshRate={600} className={"w-full h-full rounded-tremor-default"}/>
              </Card>
            </Grid>
          </TabPanel>
        </TabPanels>
      </TabGroup>
    </>
  );
}
