"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { Callout, Text, Title } from "@tremor/react";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { AirQualityMeasurement } from "@/src/types/AirsightTypes";
import Link from "next/link";

export default function Page() {
  return (
    <>
      <Title>Homepage of AIrsight</Title>
      <Text>Welcome to the AIrsight application. </Text>
      <br />
      <Text>A quick summary of the different types of data we show:</Text>
      <Text>PM1, PM2.5 and PM10 all stand for 'particulate matter' of a diameter at or less than its number. So PM10 stands for 10 micrometers or less.</Text>
      <Text>These measurements are important as particulate matter of certain sizes at a high enough concentration in the air can have negative health effects on humans.</Text>
      <Text>We show these risk areas as colored areas in our data visualisations.</Text>
      <br />
      <Text>For more reading on what each type of particulate matter means, we suggest checking out the documentation of OpenAQ.</Text>
    </>
  );
}
