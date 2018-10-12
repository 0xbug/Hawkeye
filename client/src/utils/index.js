import dayjs from "dayjs";
import "dayjs/locale/zh-cn";
import { Base64 } from "js-base64";
import relativeTime from "dayjs/plugin/relativeTime";

dayjs.extend(relativeTime);
dayjs.locale("zh-cn");

export const timeAgo = time => {
  return dayjs().from(dayjs(time));
};

export const dateFormat = time => {
  return dayjs(time).format("YYYY-MM-DD HH:mm");
};
export const dateTimeFormat = time => {
  return dayjs(time).format("YYYY-MM-DD");
};
export const b64Decode = val => {
  return Base64.decode(val);
};
export const toThousands = num => {
  return (num || 0).toString().replace(/(\d)(?=(?:\d{3})+$)/g, "$1,");
};
