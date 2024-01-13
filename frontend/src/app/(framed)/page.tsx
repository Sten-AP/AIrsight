"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { Callout, Text, Title } from "@tremor/react";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { AirQualityMeasurement } from "@/src/types/AirsightTypes";

export default function Page() {
  return (
    <>
      <Title>Homepage of AIrsight</Title>
      <Text>Lorem ipsum dolor sit amet, consetetur sadipscing elitr.</Text>
    </>
  );
}
