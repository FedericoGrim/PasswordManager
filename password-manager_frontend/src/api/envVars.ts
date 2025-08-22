import { env } from 'next-runtime-env';

const getEnvVar = (key: string, fallbackValue: string | undefined) => {
  return (env('NEXT_PUBLIC_' + key) || fallbackValue)!;
}

const getIntEnvVar = (key: string, fallbackValue: string | undefined) => {
  return parseInt(getEnvVar(key, fallbackValue));
}

export { getEnvVar, getIntEnvVar };
