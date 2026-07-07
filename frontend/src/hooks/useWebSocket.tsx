// WebSocket hook for StadiumVerse Intelligence OS
import React, { createContext, useContext, useState, useEffect } from 'react';

type EventHandler = (data: unknown) => void;

interface MockSocket {
  on: (event: string, callback: EventHandler) => void;
  off: (event: string, callback: EventHandler) => void;
  emit: (event: string, data: unknown) => void;
}

interface WebSocketContextType {
  socket: MockSocket | null;
  isConnected: boolean;
}

const WebSocketContext = createContext<WebSocketContextType>({
  socket: null,
  isConnected: false,
});

interface WebSocketProviderProps {
  url: string;
  children: React.ReactNode;
}

export const WebSocketProvider: React.FC<WebSocketProviderProps> = ({ url, children }) => {
  const [socket, setSocket] = useState<MockSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);

  useEffect(() => {
    // Simulated WebSocket connection — production would connect to the real endpoint
    setIsConnected(true);

    const mockSocket: MockSocket = {
      on: (_event: string, _callback: EventHandler) => {
        // Register listener — production implementation
      },
      off: (_event: string, _callback: EventHandler) => {
        // Deregister listener — production implementation
      },
      emit: (_event: string, _data: unknown) => {
        // Emit event — production implementation
      },
    };

    setSocket(mockSocket);

    return () => {
      setIsConnected(false);
      setSocket(null);
    };
  }, [url]);

  return (
    <WebSocketContext.Provider value={{ socket, isConnected }}>
      {children}
    </WebSocketContext.Provider>
  );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useWebSocket = () => {
  const context = useContext(WebSocketContext);
  if (!context) {
    throw new Error('useWebSocket must be used within a WebSocketProvider');
  }
  return context;
};
