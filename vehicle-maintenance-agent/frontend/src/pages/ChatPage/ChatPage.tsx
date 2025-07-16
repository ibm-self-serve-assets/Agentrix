import { useState, useEffect } from "react";


import useChatBot from "../../hooks/useChatBot";
import ChatContainer from "../../components/ChatContainer/ChatContainer";
import ChatMessage from "../../components/ChatMessage/ChatMessage";
import "./ChatPage.scss";
import { Column, Row } from "@carbon/react";
import {chatOrchestrateStream } from "../../services/llm.service";
import SamplePrompt from "../../components/SamplePrompt/SamplePrompt";





const ChatPage = () => {
  let defaultMessage = import.meta.env.VITE_WELCOME_MESSAGE
  const [threadId, setThreadId] = useState("")
  const [loading, setLoading] = useState(false)

 type ChatStreamParams = {
  onChunk?: (chunk: any) => void;
  onError?: (error: any) => void;
};

const wrappedChatOrchestrate = async (
  query: string,
  threadId: string,
  extraParams: ChatStreamParams
): Promise<void> => {
  await chatOrchestrateStream(query, threadId, {
    onChunk: extraParams.onChunk,
    onError: extraParams.onError,
  });
};

  const { messages, waiting, sendMessage, newChat, toggleReasoningFlag } = useChatBot({ defaultMessage, senderType: "assistant", getResponse: wrappedChatOrchestrate })


  const samplePrompts = [
   "What does the engine temperature warning light mean?",
   "My car is shaking and I have the engine temperature warning light on can you diagnose it?",
   "Where is the nearest service center?"
  ]
  
useEffect(() => {

  if (messages.length > 2) {
    setThreadId(messages[2]?.threadId ?? '');
  } else {
    setThreadId('');
  }
}, [messages]); // ✅ Trigger effect when messages change



  const submit = async (message: string) => {


  setLoading(true);
  try {
    await sendMessage({ message, threadId });
    setLoading(false);
  } catch (err) {
    console.error("Send message failed", err);
  } finally {
    setLoading(false);
  }
};


  const copyChatToClipboard = () => {
    // setInlineToastMsg(false);

    const chatText = messages
      .map((message) => {
        const senderPrefix = message.sender === "user" ? "You: " : "watsox: ";
        return `${senderPrefix}${message.text}`;
      })
      .join("\n\n"); // Join messages with line breaks


    navigator.clipboard.writeText(chatText).then(() => {
      // setInlineToastMsg(true);
      // setNotificationKind("success");
      // setNotificationTitle("Chat copied to clipboard!")
    }).catch(err => {
      console.error("Failed to copy chat:", err);
      // setNotificationKind("error");
      // setNotificationTitle("Failed to copy chat!")
    });

  };

  return (
    <>
     
          
     

      <ChatContainer
        copyChatToClipboard={copyChatToClipboard}
        handleNewChat={() => { setThreadId(""); newChat() }}
        disableChat={import.meta.env.VITE_ENABLE_CHAT === "false" || waiting}
        getCurrentMessage={submit}>
        {/* {messages.map(message =>
          <ChatMessage message={message.message} sender={message.sender} reasoning={message.reasoning ? message.reasoning : ""} key={Math.random().toString(36).substring(2, 5)} />

        )} */}
        {messages.map((chat, i) =>
          <ChatMessage
            // key={i}
            key={Math.random().toString(36).substring(2, 5)} 
            messages={chat?.messages}
            sender={chat.sender}
            reasoning={chat.reasoning || ""}
            event={chat} // ✅ pass event
            stepDetails={chat.stepDetails || []} // ✅ pass stepDetails
            responseType={chat.responseType} // ✅ pass responseType
            loading={chat?.messages?.length > 0  && chat?.messages?.some(m => m.text === '')  && waiting}
            reasoningFlag={chat.reasoningFlag}
            onToggleReasoning={() => {
              toggleReasoningFlag(i)}} // ✅ pass toggle handler
          />
        )}
        <Row >
          {!waiting && samplePrompts.map(prompt =>
            <Column md={2} key={prompt} style={{ margin: '0.5rem' }}>
              <SamplePrompt message={prompt} sendMessage={() => {
                setLoading(true); 
                sendMessage({ message: prompt, threadId });
              }} disabled={waiting} threadId={threadId} />
            </Column>
          )}
        </Row>
        {waiting && <ChatMessage messages={[]} sender="watsonx" reasoning={""} loading={loading} responseType="" reasoningFlag="" onToggleReasoning={() => { }} />}
       
      </ChatContainer>

      {/* {loading &&
        // <Loading withOverlay={true}></Loading>
        <div className="loading-overlay">
          <div className="loading-content">
            <CircleLoader
              color={'blue'}
              loading={true}
              size={50}
              aria-label="Loading Spinner"
              data-testid="loader"
            />
            <span>Please wait, initializing chat session...</span>
          </div>
        </div>
      } */}
    </>
  );
};


export default ChatPage