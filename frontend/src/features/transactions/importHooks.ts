import { useMutation, useQueryClient } from "@tanstack/react-query";
import { confirmImport, previewImport } from "./importApi";

export function usePreviewImport() {
  return useMutation({
    mutationFn: previewImport,
  });
}

export function useConfirmImport() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: confirmImport,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["transactions"] });
    },
  });
}