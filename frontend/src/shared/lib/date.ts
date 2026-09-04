const dateTimeFormatter = new Intl.DateTimeFormat("es-ES", {
  dateStyle: "medium",
  timeStyle: "short",
  timeZone: "Europe/Madrid",
});

const dateFormatter = new Intl.DateTimeFormat("es-ES", {
  dateStyle: "medium",
  timeZone: "Europe/Madrid",
});

export const formatDateTime = (value: string): string => dateTimeFormatter.format(new Date(value));
export const formatDate = (value: string): string =>
  dateFormatter.format(new Date(`${value}T12:00:00`));
