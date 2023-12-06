import { useEffect, useRef, useState } from "react";
import {
  QueryFunction,
  QueryKey,
  useQuery as originalUseQuery,
  UseQueryOptions,
  UseQueryResult,
} from "react-query";

const VISUAL_LOADING_TIMEOUT = 600;

type ExtendedUseQueryResult<TData, TError> = UseQueryResult<TData, TError> & {
  isLoadingVisual: boolean;
};

export function useQuery<
  TQueryFnData = unknown,
  TError = unknown,
  TData = TQueryFnData,
  TQueryKey extends QueryKey = QueryKey
>(
  queryKey: TQueryKey,
  queryFn: QueryFunction<TQueryFnData, TQueryKey>,
  options?: UseQueryOptions<TQueryFnData, TError, TData, TQueryKey>
): ExtendedUseQueryResult<TData, TError> {
  const queryResult = originalUseQuery<TQueryFnData, TError, TData, TQueryKey>(
    queryKey,
    queryFn,
    options
  );
  const [isLoadingVisual, setLoadingVisual] = useState(false);

  const isLoadingRef = useRef(queryResult.isLoading);
  isLoadingRef.current = queryResult.isLoading;

  useEffect(() => {
    if (!queryResult.isLoading) {
      setLoadingVisual(false);
      return;
    }

    setTimeout(() => {
      if (!isLoadingRef.current) return;

      setLoadingVisual(true);
    }, VISUAL_LOADING_TIMEOUT);
  }, [queryResult.isLoading]);

  return { ...queryResult, isLoadingVisual };
}