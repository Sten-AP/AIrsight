import GrafanaFrame from "../../components/grafanaFrame";

export default function Page() {
  return (
    <>
      <GrafanaFrame className={"min-w-full"} panelId={9} style={{height: "calc(100vh - 64px) !important"}}/>    
    </>
  );
}