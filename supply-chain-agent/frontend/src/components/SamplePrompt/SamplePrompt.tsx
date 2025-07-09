import { ClickableTile} from "@carbon/react"
import {ArrowRight} from "@carbon/icons-react"
import "./SamplePrompt.scss"
type SamplePromptProps = {
    message: string,
    sendMessage: Function,
    disabled: boolean,
    threadId: string
}

const SamplePrompt = ({ message, sendMessage, disabled, threadId}: SamplePromptProps) => {
    return <ClickableTile className="prompt-tile" onClick={() => sendMessage({message, threadId})} disabled={disabled}>
        <p style={{fontSize: "12px"}}>{message}</p>
        <div style={{float: "right", marginBottom: "0.5rem"}}>
        <ArrowRight fill="#5d7aab" style={{position:"absolute", bottom: "1rem", right:"1rem"}}/>
        </div>
    </ClickableTile>
}

export default SamplePrompt