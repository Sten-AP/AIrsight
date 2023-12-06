import axios from "axios";

const fetchApi = async (
  method: "GET" | "POST" | "PUT" | "DELETE",
  url: string,
  body: object | null = null,
): Promise<any> => {
  let baseURL = "https://airsight.cloudsin.space/api";

  const response = await axios({
    url: `${baseURL}${url}`,
    data: body,
    responseType: "json",
    // When necessary we can add tokens here.
    // headers: {
    //   Authorization: `Bearer ${token}`,
    // },
    method,
    validateStatus: (status) =>
      (status >= 200 && status < 300) || status === 404,
  });

  if (response.status == 404) {
    return undefined;
  }

  return response.data;
};

const queryGenerator = (query: object) =>
  Object.entries(query).length > 0
    ? `?${Object.entries(query)
        .map(([key, value]) => `${key}=${encodeURIComponent(value)}`)
        .join("&")}`
    : "";

export const get = (
  url: string,
  query: object = {},
) => fetchApi("GET", `${url}${queryGenerator(query)}`, null);
export const post = (url: string, body: object) => fetchApi("POST", url, body);
export const put = (url: string, body: object) => fetchApi("PUT", url, body);
export const del = (url: string) => fetchApi("DELETE", url);