import { AILabel, AILabelContent } from "@carbon/react"

interface CustomAILabelProps {
    name: string
}

const CustomAILabel = ({name}:CustomAILabelProps) => {
    return <AILabel className="slug-container">

        <AILabelContent className="test-label">
            <strong> Model used: </strong> {name}
        </AILabelContent>
    </AILabel>
}

export default CustomAILabel;