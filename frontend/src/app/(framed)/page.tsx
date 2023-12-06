"use client";
import { useLocations } from "@/src/hooks/locations";
import { Callout, Text, Title } from "@tremor/react";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";


export default function Page() {
  const { data: locations, isSuccess, isLoadingVisual, isError } = useLocations();
  return (
    <>
      <Title>Homepage of AIrsight</Title>
      <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr.</Text>

      {isLoadingVisual &&
      <Callout
      className="h-12 mt-4"
      title="Loading locations"
      icon={ExclamationCircleIcon}
      color="rose"
    >
      Loading locations
    </Callout>
      }
      {isSuccess &&
      locations &&
      locations.map(location => (
        <p>{location}</p>
      ))}
    </>
  );
}
