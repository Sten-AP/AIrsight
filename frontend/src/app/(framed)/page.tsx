"use client";
import { useEffect, useState } from "react";
import axios from "axios";
import { Callout, Card, Grid, Subtitle, Text, Title } from "@tremor/react";
import { ExclamationCircleIcon } from "@heroicons/react/24/outline";
import { AirQualityMeasurement } from "@/src/types/AirsightTypes";
import Link from "next/link";

export default function Page() {
  return (
    <>
      <Title>AIrsight</Title>
      <Text>Welcome to the AIrsight platform. </Text>
      <Grid numItemsMd={2} className='mt-6 gap-6'>
        <Card>
          <Subtitle className='mb-2'>About</Subtitle>
          <Text>This web application is a part of the AIrsight project. Created as a research project for our Minor in Artificial Intelligence at AP Hogeschool Antwerp.</Text>
          <Text className='my-1'>Realised by the following students:</Text>
          <Text>Joppe van Belleghem, Viral Ganga Persad, Sten Hulsbergen and Jelle Spruyt.</Text>
          <br />
          <Subtitle className='mb-2'>In short</Subtitle>
          <Text>A quick summary of the different types of data we show:</Text>
          <Text>PM1, PM2.5 and PM10 all stand for 'particulate matter' of a diameter at or less than its number. So PM10 stands for 10 micrometers or less.</Text>
          <Text>These measurements are important as particulate matter of certain sizes at a high enough concentration in the air can have negative health effects on humans.</Text>
          <Text>We show these risk areas as colored areas in our data visualisations.</Text>
          <br />
          <Text>For more reading on what each type of particulate matter means, we suggest checking out the documentation of OpenAQ.</Text>
        </Card>
        <Card>
          <Subtitle className='mb-2'>Introducing AIrsight</Subtitle>
          <iframe
            className='w-full rounded-lg'
            width='auto'
            height='350'
            src='https://www.youtube.com/embed/ByNyhPcw4Lg?si=6VeYOgzIXKZf8pg4'
            title='YouTube video player'
            frameBorder='0'
            allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share'
            allowFullScreen></iframe>
        </Card>
      </Grid>
      <br />
    </>
  );
}
