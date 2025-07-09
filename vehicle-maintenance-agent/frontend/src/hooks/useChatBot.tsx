import { useState, useRef } from "react";

type ToolStepNew = {

  tool_calls: any;
  tool_response: any;
};

type Message = {
  text: string,
  type: string
}

type ChatbotMessage = {
  [x: string]: any;
  sender: string;
  messages: Message[];
  reasoning?: string;
  reasoningFlag: any;
  event?: string;
  stepDetails?: ToolStepNew[];
  responseType?: string;
  threadId: string;
};

type UseChatbotProps = {
  defaultMessage: string;
  senderType: string;
  getResponse: (
    query: string,
    threadId: string,
    extraParams: {
      onChunk?: (chunk: string | any) => void;
      onError?: (error: any) => void;
    }
  ) => Promise<void>;
};

// type DataItem = {
//   question: string;
//   content: any;
//   step_details?: any;
// };

const useChatBot = ({ defaultMessage, senderType, getResponse }: UseChatbotProps) => {
  const [messages, setMessages] = useState<ChatbotMessage[]>([
    {
      messages: [{ text: defaultMessage, type: "text" }],
      sender: senderType,
      reasoningFlag: null, threadId: ''
    }])
  const [waiting, setWaiting] = useState<boolean>(false);
  const tempStepRef = useRef<any[]>([]); // 🔁 Store stepDetails temporarily
  const hasSeenThinkingStep = useRef(false);
  const currentStreamBuffer = useRef(""); // To accumulate streamed delta text



  //   const [threadId, setThreadId] = useState<string | null>(null);
  const toggleReasoningFlag = (index: number) => {
    setMessages(prev => {
      const updated = [...prev];
      const message = updated[index];
      updated[index] = {
        ...message,
        reasoningFlag: message.reasoningFlag === true ? false : true,
      };
      return updated;
    });
  };

  
  /*function transformStepDetailsRaw(stepHistory: any[]): {
    tool_call: any;
    tool_response: string;
  }[] {
    const result: { tool_call: any; tool_response: string }[] = [];

    const toolCallMap: Record<string, any> = {};
    const toolResponseMap: Record<string, string> = {};

    for (const step of stepHistory) {
      const stepDetails = step.step_details || [];

      for (const detail of stepDetails) {
        // Case 1: type === "tool_calls" with embedded array
        if (detail.type === "tool_calls" && Array.isArray(detail.tool_calls)) {
          for (const call of detail.tool_calls) {
            if (call.id) {
              toolCallMap[call.id] = call.args;
            }
          }
        }

        // Case 2: flat tool_call and tool_response
        if (detail.type === "tool_call" && detail.tool_call_id) {
          toolCallMap[detail.tool_call_id] = detail;
        }

        if (detail.type === "tool_response" && detail.tool_call_id) {
          toolResponseMap[detail.tool_call_id] = detail.content;
        }
      }
    }

    // Merge matched pairs
    for (const id of Object.keys(toolCallMap)) {
      result.push({
        tool_call: toolCallMap[id],
        tool_response: toolResponseMap[id] || ""
      });
    }

    return result;
  }*/



  const sendMessage = async ({ message, threadId }: { message: string; threadId: string }) => {
    setMessages(prev => [...prev, {
      messages: [{ text: message, type: "text" }],
      sender: "user",
      reasoningFlag: false,
      threadId
    }]);
    setWaiting(true);

    try {
      await getResponse(message, threadId, {
        onChunk: (chunk: any) => {
          const stepDetail = chunk?.data?.delta?.step_details;
          const deltaContent = chunk?.data?.delta?.content ?? [];

          setMessages((prev) => {
            const last = prev[prev.length - 1];
            const updatedStepDetails = [...(last?.stepDetails || [])];

            // 🧠 run.step.thinking — tool_calls detected
            if (stepDetail && chunk.event?.startsWith("run.step.thinking")) {
              hasSeenThinkingStep.current = true;

              const step = stepDetail[0];
              if (step?.tool_calls?.length > 0) {
                const newStep = {
                  tool_calls: step.tool_calls[0],
                  tool_response: null,
                };

                console.log("🧠 Buffering tool_calls in tempStepRef", newStep);
                tempStepRef.current.push(newStep);
              }

              return prev;
            }

            // 🛠 run.step.delta — update tool_calls/tool_response
            if (stepDetail && chunk.event?.startsWith("run.step.delta")) {
              const step = stepDetail[0];

              // Case 1: Update stepDetails if assistant message already exists
              if (last?.sender === "assistant" && updatedStepDetails.length > 0) {
                for (let i = updatedStepDetails.length - 1; i >= 0; i--) {
                  if (!updatedStepDetails[i].tool_calls && step.tool_calls) {
                    updatedStepDetails[i].tool_calls = step.tool_calls[0];
                  }

                  if (!updatedStepDetails[i].tool_response && (step.tool_response || step.content)) {
                    updatedStepDetails[i].tool_response = step.tool_response || step.content || '';
                  }

                  if (updatedStepDetails[i].tool_calls && updatedStepDetails[i].tool_response) break;
                }

                return [
                  ...prev.slice(0, -1),
                  {
                    ...last,
                    stepDetails: updatedStepDetails,
                    messages: last.messages || [],
                    responseType: chunk.event,
                    threadId: chunk.data?.thread_id,
                  },
                ];
              }

              // Case 2: No assistant message yet — update buffer
              if (
                tempStepRef.current.length === 0 &&
                (step.tool_calls || step.tool_response || step.content)
              ) {
                tempStepRef.current.push({
                  tool_calls: step.tool_calls[0] || null,
                  tool_response: step.tool_response || step.content || '',
                });
              }

              for (let i = tempStepRef.current.length - 1; i >= 0; i--) {
                if (!tempStepRef.current[i].tool_calls && step.tool_calls) {
                  tempStepRef.current[i].tool_calls = step.tool_calls[0];
                }

                if (!tempStepRef.current[i].tool_response && (step.tool_response || step.content)) {
                  tempStepRef.current[i].tool_response = step.tool_response || step.content || '';
                }

                if (tempStepRef.current[i].tool_calls && tempStepRef.current[i].tool_response) break;
              }

              return prev;
            }

            // 🌀 message.delta — just accumulate text
            if (Array.isArray(deltaContent) && deltaContent.length > 0) {
              const incomingText = deltaContent.map(entry => entry.text).join("");
              currentStreamBuffer.current += incomingText;
              return prev; // Don't update messages yet
            }

            // 🧩 message.created or run.step.completed — now push final message
            if (chunk.event === "message.created" || chunk.event === "run.step.completed") {
              const finalText = currentStreamBuffer.current.trim();
              currentStreamBuffer.current = ""; // reset buffer

              const shouldMergeText = hasSeenThinkingStep.current;
              hasSeenThinkingStep.current = false;

              const parsedMessages = shouldMergeText
                ? [{ text: finalText, type: "text" }]
                : finalText.split(/(?<=[.!?])\s+/).map((sentence) => ({
                  text: sentence,
                  type: "text",
                }));

              if (last?.sender === "assistant") {
                return [
                  ...prev.slice(0, -1),
                  {
                    ...last,
                    messages: [...(last.messages || []), ...parsedMessages],
                    stepDetails: last.stepDetails || [],
                    responseType: chunk.event,
                    threadId: chunk.data?.thread_id,
                  },
                ];
              }

              const bufferedSteps = [...tempStepRef.current];
              tempStepRef.current = [];

              return [
                ...prev,
                {
                  sender: "assistant",
                  messages: parsedMessages,
                  stepDetails: bufferedSteps,
                  responseType: chunk.event,
                  reasoningFlag: false,
                  threadId: chunk.data?.thread_id,
                },
              ];
            }

            return prev;
          });

        },
        onError: (err) => {
          console.error("Something went wrong with the response", err);
          setMessages(prev => [
            ...prev,
            {
              messages: [{ text: 'Something went wrong. Please try again', type: "text" }],
              sender: "assistant",
              reasoningFlag: null,
              threadId,
            }
          ]);
        }
      });
    } catch (err) {
      console.error("sendMessage error:", err);
    } finally {
      setWaiting(false);
    }
  };

  const newChat = () => {
    setMessages([{
      messages: [{ text: defaultMessage, type: "text" }],
      sender: senderType, reasoningFlag: false, threadId: ''
    }]);
  };

  return { messages, waiting, sendMessage, newChat, toggleReasoningFlag };
};

export default useChatBot;
