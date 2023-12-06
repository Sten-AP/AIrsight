export interface Region {
  code: string;
  regions: string[];
}

export type Country = {
  [key: string]: {
    code: string;
    regions: string[];
  };
};

export type LocationData = Country[];