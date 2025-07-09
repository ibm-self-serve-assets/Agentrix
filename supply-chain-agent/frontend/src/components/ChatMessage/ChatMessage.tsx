import { Accordion, AccordionItem, Button, CodeSnippet, Link } from "@carbon/react"
import Markdown from "markdown-to-jsx"
import "./ChatMessage.scss";
import { downloadPdf } from "../../services/llm.service";
import { JSXElementConstructor, Key, ReactElement, ReactNode, ReactPortal, useEffect, useState } from "react";
import { PulseLoader } from "react-spinners";
// type ChatMessageProps = {
//   message: string,
//   sender: string,
//   reasoning : string,
// }
type ToolStep = {
  // type: string;
  tool_calls: any; // array tool_calls: any;
  tool_response: any;
  // content: any
};

// type ToolCall = {
//   id: string;
//   name: string;
//   args: {
//     query: string;
//   };
// };
type Message = {
  text: string,
  type: string
}

type ChatMessageProps = {
  messages: Message[];
  sender: string;
  reasoning: string;
  event?: any;
  stepDetails?: ToolStep[];
  responseType?: string;
  loading: boolean;
  reasoningFlag: any;
  onToggleReasoning: Function
};



const ChatMessage = ({ messages, sender, reasoning, stepDetails = [], loading, reasoningFlag , onToggleReasoning}: ChatMessageProps) => {
  // console.log('event', event, stepDetails, responseType, loading)
 
const [currentTime, setCurrentTime] = useState(
  new Date().toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  }).toUpperCase()
);

useEffect(() => {
  const timer = setInterval(() => {
    setCurrentTime(new Date().toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    }).toUpperCase());
  }, 1000);

  return () => clearInterval(timer);
}, []);



  const downloadReport = async () => {
    const data = await downloadPdf();
    const url = window.URL.createObjectURL(data);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "portfolio_report.pdf");
    document.body.appendChild(link);
    link.click();
    link.remove();
  };

  useEffect(() => {

    // if (isMarkdownTable(message)) {
    //   console.log("This message contains a markdown table");
    // } else {
    //   console.log("No markdown table found");
    // }
  }, [loading])





  if (sender !== "user" ) {
    return (
      <div className="sender">
          <div style={{ display: "flex" }}>
            <img src="./watsonx-app-icon-dark-mode.svg" height={28} width={28} alt="" />
            <span style={{ marginLeft: "1rem" }}>
              {import.meta.env.VITE_APP_NAME} 
                  {messages?.length > 0 && (
                     <>
                    | {currentTime}
                 
              <Link style={{ marginLeft: '0.5rem', cursor: 'pointer' }} onClick={() => {
                onToggleReasoning()}}>{reasoningFlag === false
                ? '| Show reasoning'
                : reasoningFlag === true
                  ? '| Hide reasoning'
                  : null}
              </Link>
              </>
               )}
            </span>
          </div>
     

        <div style={{ padding: "0.5rem",marginLeft: "1rem"}}>

          {loading && messages?.length == 0 ? (<>
          {/* <TagSkeleton style={{ color: 'blue' }}></TagSkeleton> */}
           <PulseLoader
           style={{marginLeft: "1rem"}}
              color={'blue'}
              loading={true}
              size={15}
              aria-label="Loading Spinner"
              data-testid="loader"
            />
          {/* Reasoning */}
          </>) : (
            <>
              <div>
                {/* ========== EVENT: run.step.delta ========== */}
                {reasoningFlag === true && (
                  <>
                   {stepDetails.length > 0 && (
                      <div className="condition-flow" style={{ padding: "1rem" }}>

                        <Accordion className="tool-steps-accordion" align="start">
                          {stepDetails.map((step, idx) => (
                            <AccordionItem key={idx} title={`Step ${idx + 1}`}>
                              <div style={{ marginBottom: "1rem" }}>
                                {/* Tool Info */}
                                <div style={{ marginBottom: "0.5rem" }}>
                                  <p><strong>Tool:</strong> {step?.tool_calls?.name}</p>
                                  <p><strong>Query:</strong> {step?.tool_calls?.args?.query}</p>
                                </div>

                                {/* Tool Call Input */}
                                {step?.tool_calls?.args && (
                                  <>
                                    <div
                                      style={{
                                        backgroundColor: '#484848',
                                        color: '#ffffff',
                                        padding: '0.5rem 1rem',
                                        borderTopLeftRadius: '0.25rem',
                                        borderTopRightRadius: '0.25rem',
                                        fontWeight: 'bold',
                                        fontFamily: 'IBM Plex Mono, monospace',
                                      }}
                                    >
                                      Input
                                    </div>
                                    <CodeSnippet type="multi" wrapText>
                                      {JSON.stringify(step?.tool_calls?.args, null, 2)}
                                    </CodeSnippet>
                                  </>
                                )}

                                {/* Tool Response Output */}
                                {step.tool_response && (
                                  <>
                                    <div
                                      style={{
                                        backgroundColor: '#484848',
                                        color: '#ffffff',
                                        padding: '0.5rem 1rem',
                                        borderTopLeftRadius: '0.25rem',
                                        borderTopRightRadius: '0.25rem',
                                        fontWeight: 'bold',
                                        fontFamily: 'IBM Plex Mono, monospace',
                                        marginTop: '1rem',
                                      }}
                                    >
                                      Output
                                    </div>
                                    <CodeSnippet type="multi" wrapText>
                                      {step?.tool_response}
                                    </CodeSnippet>
                                  </>
                                )}
                              </div>
                            </AccordionItem>
                          ))}
                        </Accordion>

                      </div>
                )}
                  </>
                )}
               

                {/* ========== EVENT: message.delta ========== */}
                {/* { (message !== "" || !responseType || responseType === "thread.message.delta") && responseType === "conversational_search" && (
            <Markdown options={{
              overrides: {
                h1: { component: ({ children }) => <h1 style={{ margin: "0.5rem 0" }}>{children}</h1> },
                h2: { component: ({ children }) => <h2 style={{ margin: "0.5rem 0" }}>{children}</h2> },
                h3: { component: ({ children }) => <h3 style={{ margin: "0.5rem 0" }}>{children}</h3> },
                h4: { component: ({ children }) => <h4 style={{ margin: "0.5rem 0" }}>{children}</h4> },
                h5: { component: ({ children }) => <h5 style={{ margin: "0.5rem 0" }}>{children}</h5> },
                h6: { component: ({ children }) => <h6 style={{ margin: "0.5rem 0" }}>{children}</h6> },

                table: {
                  component: ({ children }) => (
                    <table
                      style={{
                        borderCollapse: "collapse",
                        width: "100%",
                        border: "1px solid white",
                        margin: "0 0 1rem 0"
                      }}
                    >
                      {children}
                    </table>
                  ),
                },
                thead: {
                  component: ({ children }) => (
                    <thead >{children}</thead>
                  ),
                },
                th: {
                  component: ({ children }) => (
                    <th
                      style={{
                        padding: "1rem",
                        border: "1px solid white",
                        textAlign: "left",
                      }}
                    >
                      {children}
                    </th>
                  ),
                },
                td: {
                  component: ({ children }) => (
                    <td
                      style={{
                        padding: "1rem",
                        border: "1px solid white",
                      }}
                    >
                      {children}
                    </td>
                  ),
                },
              },
            }}
              style={{ fontSize: "16px" }}>{message.replaceAll("WatsonX", "watsonx")}</Markdown>
          )} */}

                {/* ========== EVENT: message.created ========== */}
                {/* {responseType === "thread.message.created" && (
                  <Tile className="message-tile">
                    {messages.map((msg: { message: any, type: any }, index: Key | null | undefined) => (
                      <Markdown
                        key={index}
                        options={{
                          overrides: {
                            table: {
                              component: ({ children }) => (
                                <table style={{ borderCollapse: "collapse", width: "100%", border: "1px solid white", marginBottom: "1rem" }}>{children}</table>
                              )
                            },
                            th: {
                              component: ({ children }) => (
                                <th style={{ padding: "1rem", border: "1px solid white", textAlign: "left" }}>{children}</th>
                              )
                            },
                            td: {
                              component: ({ children }) => (
                                <td style={{ padding: "1rem", border: "1px solid white" }}>{children}</td>
                              )
                            }
                          }
                        }}
                      >
                        {msg.text}
                      </Markdown>
                    ))}
                  </Tile>
                )} */}

                {/* ========== Download Button Trigger Condition ========== */}
                {reasoning.includes("save_pdf_to_disk") && (
                  <Button kind="tertiary" onClick={downloadReport} style={{ marginTop: "1rem" }}>
                    Download Report
                  </Button>
                )}
              </div>
              {/* normal message show */}
               <div className="default-flow" style={{ padding: '1rem' }}>
                {messages?.map((msg: any, index) => (
                  <Markdown
                    key={index}
                    options={{
                      forceBlock: true,
                      overrides: {
                        table: {
                          component: ({ children }) => (
                            <table style={{ borderCollapse: 'collapse', width: '100%', border: '1px solid white' }}>{children}</table>
                          ),
                        },
                        th: {
                          component: ({ children }) => (
                            <th style={{ border: '1px solid #ccc', padding: '0.5rem' }}>{children}</th>
                          ),
                        },
                        td: {
                          component: ({ children }) => (
                            <td style={{ border: '1px solid #ccc', padding: '0.5rem' }}>{children}</td>
                          ),
                        },
                      },
                    }}
                  >
                    {msg?.text}
                  </Markdown>
                ))}
              </div>
            </>)}
        </div>
      </div>
    );
  }

  // ========== USER MESSAGE ==========
  return (
    <div className="receiver">
      <div>
        <div className="chat-message-details">
          <span>You | {currentTime} </span></div>
        <div className="_w3--chat-message__content_i5j4f_35">
          <div className="chat-bubble">
            {messages?.map((msg: { text: string | number | boolean | ReactElement<any, string | JSXElementConstructor<any>> | Iterable<ReactNode> | ReactPortal | null | undefined; }, index: Key | null | undefined) => (
              <p key={index} style={{ fontSize: "14px" }}>{msg?.text}</p>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};


// const ChatMessage = ({ message, sender, reasoning}: ChatMessageProps) => {

//   const downloadReport = async () => {
//     try {
//       let data = await downloadPdf()
//       console.log(data, "----")
//       const url = window.URL.createObjectURL(data)

//     const link = document.createElement('a');
//     link.href = url;
//     link.setAttribute(
//       'download',
//       `portfolio_report.pdf`,
//     );

//     // Append to html link element page
//     document.body.appendChild(link);

//     // Start download
//     link.click();

//     // Clean up and remove the link
//     link.parentNode?.removeChild(link);
//     } catch {

//     }
//   }

//   return <>{sender != "user" ?
//     <div className="sender">
//       <div style={{ display: 'flex', justifyContent: '' }}>
//         <div>
//           <img src={"./watsonx-app-icon-dark-mode.svg"} height={28} width={28} alt="" className="_w3--watsonx-avatar_18pme_1" />
//         </div>
//         <div style={{ alignContent: 'center' }}> <span style={{ marginLeft: "1rem", alignContent: "center" }}>watsonx</span></div>
//       </div>


//       <div style={{ padding: "1rem" }}>
//         {message == "" ? (<TagSkeleton style={{ color: 'blue' }}></TagSkeleton>) : (
//           <>
//             <p className="Markdown-module--paragraph--29381 Markdown-module--paragraph--responsive--7fcac"
//               style={{ paddingLeft: "1rem" }}>
//               <Markdown style={{ fontSize: '16px' }}>{message.replaceAll("WatsonX", "watsonx")}</Markdown>
//             </p>
//             {reasoning && <Accordion className="reason">
//               <AccordionItem title="How did I get this answer?"><Markdown style={{ fontSize: '16px' }}>{reasoning}</Markdown></AccordionItem>
//             </Accordion>}
//             {reasoning.includes("save_pdf_to_disk") && <Button kind="tertiary" onClick={downloadReport} style={{marginTop: "1rem"}}>Download Report</Button>}
//           </>
//         )}
//       </div>
//     </div>
//     :
//     <div className="receiver">
//       <div>
//         <div className="chat-message-details">
//           <span>You </span></div>
//         <div className="_w3--chat-message__content_i5j4f_35">
//           <div className="chat-bubble">
//             <p style={{ fontSize: "14px" }}>{message}</p>
//           </div>
//         </div>
//       </div>
//     </div>
//   }</>
// }

export default ChatMessage