const getEnvVar = (_key: string, fallbackValue: string | undefined) => {
  return fallbackValue!;
}

const getIntEnvVar = (key: string, fallbackValue: string | undefined) => {
  return parseInt(getEnvVar(key, fallbackValue));
}

export { getEnvVar, getIntEnvVar };
