

export const startChatSession = async () => {
    const url = 'https://ecombackend.1uijsxnqve2c.us-south.codeengine.appdomain.cloud/api/v1/session/create';
    console.log(url)
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'accept': 'application/json',
                'X-API-Key': 'ec',
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const askDocument = async (query: string, sessionId: string) => {
    const url = 'https://ecombackend.1uijsxnqve2c.us-south.codeengine.appdomain.cloud/api/v1/chat/generate';
    const payload = {
        session_id: sessionId,
        input_data: query
    };

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
                'X-API-Key': 'ec',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        throw error;
    }
};

export const downloadPdf = async () => {
    const url = 'https://ecombackend.1uijsxnqve2c.us-south.codeengine.appdomain.cloud/download/report';
    console.log(url)
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'X-API-Key': 'ec',
                'Content-Type': 'application/pdf'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        return await response.blob();
    } catch (error) {
        throw error;
    }
};

