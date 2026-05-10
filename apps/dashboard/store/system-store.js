import { create } from "zustand";

export const useSystemStore = create((set) => ({
  apiStatus: "checking",
  gatewayStatus: "checking",
  socketStatus: "disconnected",

  setApiStatus: (status) => set({ apiStatus: status }),
  setGatewayStatus: (status) => set({ gatewayStatus: status }),
  setSocketStatus: (status) => set({ socketStatus: status }),
}));