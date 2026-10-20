import React, { useState } from 'react';

// The emojis players can choose from!
const AVATARS = ['😎', '🤠', '👽', '👻', '🤖', '👑', '🔥', '💎'];

const ClientScreen = () => {
  const [roomCode, setRoomCode] = useState('');
  const [nickname, setNickname] = useState('');
  const [joined, setJoined] = useState(false);
  const [ws, setWs] = useState(null);
  
  // NEW: Avatar State
  const [avatar, setAvatar] = useState(AVATARS[0]);

  const [gameState, setGameState] = useState('waiting'); 
  const [currentCard, setCurrentCard] = useState(null);
  const [guess, setGuess] = useState('');
  const [actionType, setActionType] = useState('');

  const joinRoom = (e) => {
    e.preventDefault();
    if (!roomCode || !nickname) return;

    const wsUrl = window.location.hostname === 'localhost' 
      ? `ws://localhost:8000/ws/${roomCode.toUpperCase()}/${nickname}`
      : `wss://nonames-game.onrender.com/ws/${roomCode.toUpperCase()}/${nickname}`;

    const socket = new WebSocket(wsUrl);
    
    socket.onopen = () => {
      setJoined(true);
      // NEW: Send the chosen avatar to the TV immediately!
      socket.send(JSON.stringify({
        action: 'set_avatar',
        avatar: avatar
      }));
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'turn_started') {
        if (data.actor === nickname) {
          setCurrentCard(data.card);
          setActionType(data.action_type);
          setGameState('actor_prep'); 
        } else {
          setGameState('guesser_prep'); 
        }
      }

      if (data.type === 'actor_ready') {
        setGameState(prev => {
          if (prev === 'actor_prep') return 'actor_active';
          if (prev === 'guesser_prep') return 'guesser_active';
          return prev;
        });
      }

      if (data.type === 'round_over') {
        setGameState('waiting'); 
        setCurrentCard(null);    
        setActionType('');    
        setGuess('');            
      }
    };
    setWs(socket);
  };

  const startActing = () => {
    if (ws) ws.send(JSON.stringify({ action: 'actor_ready' }));
  };

  const submitGuess = (e) => {
    e.preventDefault();
    if (!guess || !ws) return;
    
    ws.send(JSON.stringify({
      action: 'submit_guess',
      player: nickname,
      guess: guess
    }));
    setGuess(''); 
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6 font-sans">
      
      {!joined && (
        <form onSubmit={joinRoom} className="bg-gray-800 p-8 rounded-2xl border-4 border-pink-500 w-full max-w-md shadow-2xl flex flex-col gap-6">
          <h2 className="text-4xl font-black text-center text-pink-400 mb-4">JOIN GAME</h2>
          
          <input type="text" placeholder="ROOM CODE" value={roomCode} onChange={(e) => setRoomCode(e.target.value)} className="w-full text-center text-3xl p-4 rounded bg-gray-700 text-yellow-400 font-black uppercase tracking-widest outline-none" maxLength={4} />
          <input type="text" placeholder="NICKNAME" value={nickname} onChange={(e) => setNickname(e.target.value)} className="w-full text-center text-2xl p-4 rounded bg-gray-700 text-white font-bold outline-none" maxLength={12} />
          
          {/* NEW: AVATAR SELECTOR */}
          <div className="w-full mt-2">
            <p className="text-center text-gray-400 font-bold mb-2">CHOOSE YOUR AVATAR:</p>
            <div className="flex justify-center gap-2 flex-wrap">
              {AVATARS.map(a => (
                <button 
                  type="button" 
                  key={a} 
                  onClick={() => setAvatar(a)}
                  className={`text-4xl p-2 rounded-xl transition-all ${avatar === a ? 'bg-pink-500 scale-110 shadow-lg' : 'bg-gray-700 hover:bg-gray-600 opacity-50'}`}
                >
                  {a}
                </button>
              ))}
            </div>
          </div>

          <button type="submit" className="w-full bg-blue-600 hover:bg-blue-500 text-white text-3xl font-bold py-5 rounded-full mt-4 hover:scale-105 transition-all">ENTER</button>
        </form>
      )}

      {joined && gameState === 'waiting' && (
        <div className="text-center">
          <h2 className="text-5xl font-black text-yellow-400 mb-6 tracking-wide">YOU'RE IN!</h2>
          <p className="text-2xl text-gray-300 animate-pulse">Look at the main TV screen...</p>
        </div>
      )}

      {joined && (gameState === 'actor_prep' || gameState === 'actor_active') && currentCard && (
        <div className="w-full max-w-md flex flex-col items-center text-center">
          
          <div className="bg-purple-600 w-full py-4 px-4 rounded-xl mb-4 shadow-[0_0_20px_rgba(147,51,234,0.6)] animate-pulse">
            <p className="text-xl font-bold text-white uppercase tracking-widest">YOUR MISSION:</p>
            <p className="text-4xl font-black text-yellow-300">{actionType}</p>
          </div>

          <div className="bg-blue-600 w-full py-3 px-4 rounded-xl mb-6 shadow-lg">
            <p className="text-xl font-bold text-white">SAY OUT LOUD:</p>
            <p className="text-2xl font-black italic">"I'm not gonna say no names, but..."</p>
          </div>
          
          <h2 className="text-6xl font-black text-yellow-400 mb-2">{currentCard.title}</h2>
          <p className="text-xl text-gray-400 mb-8 uppercase tracking-widest">{currentCard.category}</p>
          
          <div className="bg-red-600/20 border-4 border-red-500 w-full p-6 rounded-2xl mb-8">
            <h3 className="text-3xl font-bold text-red-500 mb-4">FORBIDDEN WORDS:</h3>
            <div className="flex flex-wrap justify-center gap-2">
              {currentCard.forbidden_words.map((word, idx) => (
                <span key={idx} className="bg-red-500 text-white px-4 py-2 rounded-lg text-xl font-bold">
                  {word.toUpperCase()}
                </span>
              ))}
            </div>
          </div>

          {gameState === 'actor_prep' && (
            <button onClick={startActing} className="w-full bg-green-500 hover:bg-green-400 text-white text-5xl font-black py-6 rounded-2xl shadow-[0_0_30px_rgba(34,197,94,0.6)] hover:scale-105 transition-all animate-bounce">
              READY? GO!
            </button>
          )}
        </div>
      )}

      {joined && gameState === 'guesser_prep' && (
        <div className="text-center mt-20">
          <h2 className="text-4xl font-black text-yellow-400 mb-6">HOLD TIGHT!</h2>
          <p className="text-2xl text-gray-300 animate-pulse">Waiting for the actor to start...</p>
        </div>
      )}

      {joined && gameState === 'guesser_active' && (
        <div className="w-full max-w-md flex flex-col items-center">
          <h2 className="text-4xl font-black text-pink-400 mb-8 text-center animate-bounce">LOOK AT THE ACTOR!</h2>
          <form onSubmit={submitGuess} className="w-full flex flex-col gap-4">
            <input 
              type="text" 
              placeholder="Type your guess here..." 
              value={guess}
              onChange={(e) => setGuess(e.target.value)}
              className="w-full text-center text-2xl p-5 rounded-xl bg-gray-700 text-white font-bold focus:ring-4 focus:ring-blue-400 outline-none"
            />
            <button type="submit" className="w-full bg-yellow-500 hover:bg-yellow-400 text-gray-900 text-3xl font-black py-5 rounded-xl mt-2 hover:scale-105 transition-all">
              GUESS
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default ClientScreen;