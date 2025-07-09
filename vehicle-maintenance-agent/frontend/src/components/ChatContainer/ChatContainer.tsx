import {  Column, IconButton, Row, TextInput, Tile } from "@carbon/react"
import { Close, SendFilled, IbmWatsonxAssistant,} from '@carbon/icons-react';
import { KeyboardEventHandler, ReactNode, useEffect, useRef, useState } from "react"
import CustomAILabel from "../CustomAILabel/CustomAILabel";

type ChatContainerProps = {
    children: ReactNode
    handleNewChat: Function,
    disableChat: boolean,
    getCurrentMessage: Function
    copyChatToClipboard: Function
}

const ChatContainer = ({ children, disableChat, getCurrentMessage }: ChatContainerProps) => {

    const [message, setMessage] = useState("")
    const chatContainerRef = useRef<HTMLDivElement | null>(null);
    // const [isPanelOpen, setIsPanelOpen] = useState(true);
    useEffect(() => {

        // Scroll to the bottom of the chat container
        if (chatContainerRef.current) {
            chatContainerRef.current.scroll({
                top: chatContainerRef.current.scrollHeight,
                behavior: 'smooth'
            });
        }
    }, [children])

    const handleKeyDown: KeyboardEventHandler<HTMLInputElement> = (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            getCurrentMessage(message)
            setMessage("")
        }
    };
    // const togglePanel = () => {
    //     setIsPanelOpen(!isPanelOpen);
    // };
    

    return <Row>
        <Column sm={4} md={8} lg={16} style={{ 
            height: '100vh'
            // height: `${window.innerHeight}px`,
             }}>
            <Tile decorator={<CustomAILabel />} id="tile-1" style={{
                height: "94%", marginTop: '3rem',
                background: "linear-gradient(0deg, rgba(69, 137, 255, .2) 0%, rgba(255, 255, 255, 0) 50%), var(--cds-background, #ffffff)"
            }}>
                <header className="">
                    {/* <div style={{ float: 'right', marginRight: '2rem' }}>
                        <IconButton
                            kind="ghost"
                            size="sm"
                            style={{padding: 0}}
                            className="icon-btn"
                            onClick={() => { copyChatToClipboard() }}
                            label="Copy Chat to clipboard"
                        >
                            <Copy />
                        </IconButton>
                    </div> */}
                    {/* <div style={{ float: 'right', marginRight: '1rem' }} onClick={togglePanel}>
                        {isPanelOpen ? <SidePanelClose /> : <SidePanelOpen />}

                    </div> */}
                </header>

                <div ref={chatContainerRef} 
                style={{ height: "85%", padding: "2rem 1rem", overflow: "auto", 
                // width: "60%", 
                margin: "0 auto", scrollbarWidth: "none" }}>

                    <div style={{ textAlign: "center" }}>
                        <IbmWatsonxAssistant size="32" />
                        <p>{import.meta.env.VITE_CHATBOT_NAME}</p>
                    </div>
                    {children}

                </div>
                <Row
                    style={{ marginTop: '-6rem' }}
                >
                    <Column sm={4} md={8} lg={15} >
                        <div style={{ display: 'flex', position: 'absolute',
                             width: "90%", 
                             left: "0%", bottom: "7%" }}>
                            <TextInput
                                type="text"
                                labelText="Text input label"
                                hideLabel
                                onKeyDown={handleKeyDown}
                                placeholder="Type something"
                                disabled={disableChat}
                                onChange={(event) => {
                                    setMessage(event.target.value);
                                }
                                }
                                id="text-input-ai-label"
                                // decorator={aiLabel}
                                value={message}
                                style={{ flex: 1, paddingRight: '2rem', marginLeft: '4rem' }} // Ensure room for the icon
                            />
                            {message && (
                                <IconButton
                                    kind="ghost"
                                    size="sm"
                                    className="icon-btn"
                                    onClick={() => setMessage("")}
                                    style={{
                                        position: 'absolute',
                                        top: '28%',
                                        right: '2rem',
                                        transform: 'translateY(-50%)',
                                        // padding: 0,
                                        backgroundColor: 'transparent',
                                    }}
                                    label="Clear search"
                                >
                                    <Close size={16} />
                                </IconButton>
                            )}
                        </div>
                        <div style={{
                            padding: "0", position: 'absolute',
                            right: "12%",
                            bottom: "8%"
                        }}>
                            <IconButton
                                kind="ghost"
                                size="sm"
                                onClick={() => { getCurrentMessage(message); setMessage("") }}
                                className="icon-btn"
                                disabled={disableChat || message.trim() == ""}
                                style={{

                                }}
                                label="Enter"
                            >
                                <SendFilled size={16} />
                            </IconButton>
                        </div>
                    </Column>


                </Row>

            </Tile>

        </Column>
    </Row>
}

export default ChatContainer
