
export const transformThermometersData = (data: any[]) => {
  return data.map(({ id, name, ...rest }) => ({
    id,
    name,
    ...rest,
  }));
};
