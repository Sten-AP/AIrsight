import { CSSProperties } from "react";

export default async function GrafanaFrame({ panelId, refreshRate, style, className, timeFrame }: { panelId: number; refreshRate?: number; style?: CSSProperties; className?: string; timeFrame?: string }) {
  const baseUrl = "https://airsight.cloudsin.space/grafana/d-solo";
  const dashboardId = "bb08a297-a2d9-458a-9d7c-06258271aec3/airsight";
  const orgId = "1";
  const theme = "light";

  return <iframe className={className} style={style} src={`${baseUrl}/${dashboardId}?orgId=${orgId}&theme=${theme}&panelId=${panelId.toString()}${refreshRate ? `&refresh=${refreshRate.toString()}s` : ''}${timeFrame ? `&from=now-${timeFrame}&to=now` : ''}`}></iframe>;
}
