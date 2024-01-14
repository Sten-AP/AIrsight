import { Country } from "../types/AirsightTypes";
import { del, get, post, put } from "./client";

export const locations = (): Promise<Country[]> => get("/locations/");