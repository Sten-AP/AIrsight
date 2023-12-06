import { useQuery as useNewQuery } from "../utils/query";
import { locations } from "../api/locations";

export const useLocations = () => useNewQuery("locations", () => locations());