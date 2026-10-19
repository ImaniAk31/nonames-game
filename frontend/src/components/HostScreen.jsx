import React, { useState, useEffect, useRef } from 'react';

const HostScreen = () => {
  const [roomCode, setRoomCode] = useState('KJDS'); 
  const [players, setPlayers] = useState([]);
  
  // Game states: lobby, actor_prep, active_turn, round_over, game_over
  const [gameState, setGameState] = useState('lobby'); 
  const [ws, setWs] = useState(null);
  const [celebrationMsg, setCelebrationMsg] = useState('');
  const [timeLeft, setTimeLeft] = useState(60);

  const [maxRounds, setMaxRounds] = useState(5);
  const [currentRound, setCurrentRound] = useState(0);
  const [currentActor, setCurrentActor] = useState('SOMEONE'); 
  
  const currentRoundRef = useRef(0);
  const maxRoundsRef = useRef(5);
  useEffect(() => { currentRoundRef.current = currentRound; }, [currentRound]);
  useEffect(() => { maxRoundsRef.current = maxRounds; }, [maxRounds]);

  const tickAudioRef = useRef(null);

  const playSound = (fileName) => {
    const audio = new Audio(`/${fileName}`);
    audio.play().catch((err) => console.log("Audio play blocked by browser:", err));
  };

  const stopTickAudio = () => {
    if (tickAudioRef.current) {
      tickAudioRef.current.pause();
      tickAudioRef.current.currentTime = 0;
      tickAudioRef.current = null; 
    }
  };

  useEffect(() => {
    // --- NEW WEB DEPLOYMENT URL LOGIC ---
    const wsUrl = window.location.hostname === 'localhost' 
      ? `ws://localhost:8000/ws/${roomCode}/HOST`
      : `wss://YOUR-BACKEND-URL.onrender.com/ws/${roomCode}/HOST`;

    const socket = new WebSocket(wsUrl);
    socket.onopen = () => console.log("Host connected to WebSocket");
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'system' && data.message.includes('joined')) {
        const name = data.message.split(' ')[0]; 
        if (name !== 'HOST') {
          setPlayers((prev) => [...prev, { name: name, score: 0 }]);
        }
      } 

      if (data.type === 'turn_started') {
        setCurrentActor(data.actor);
        setGameState('actor_prep');
      }

      if (data.type === 'actor_ready') {
        setGameState('active_turn');
      }
      
      if (data.type === 'correct_guess') {
        stopTickAudio(); 
        playSound('ding.mp3'); 
        
        setCelebrationMsg(`${data.player.toUpperCase()} GOT IT RIGHT! +5 POINTS`);
        
        setPlayers((prev) => prev.map(p =>
          p.name === data.player ? { ...p, score: p.score + 5 } : p
        ));
        
        setGameState('round_over');
        socket.send(JSON.stringify({ action: 'end_round' }));

        setTimeout(() => {
          setCelebrationMsg('');
          if (currentRoundRef.current >= maxRoundsRef.current) {
            setGameState('game_over');
          } else {
            setGameState('lobby');
          }
        }, 5000);
      }
    };

    setWs(socket);
    return () => socket.close();
  }, [roomCode]);

  useEffect(() => {
    if (gameState === 'active_turn' && timeLeft === 10) {
      if (!tickAudioRef.current) {
        tickAudioRef.current = new Audio('/tick.mp3');
        tickAudioRef.current.loop = true;
        tickAudioRef.current.play().catch(e => console.log("Tick blocked", e));
      }
    }
  }, [timeLeft, gameState]);

  useEffect(() => {
    if (gameState !== 'active_turn') stopTickAudio();
  }, [gameState]);

  useEffect(() => {
    if (gameState === 'active_turn' && timeLeft > 0) {
      const timerId = setInterval(() => {
        setTimeLeft((prevTime) => prevTime - 1);
      }, 1000); 
      
      return () => clearInterval(timerId);
      
    } else if (gameState === 'active_turn' && timeLeft === 0) {
      stopTickAudio(); 
      playSound('buzzer.mp3'); 
      
      setGameState('round_over');
      if (ws) ws.send(JSON.stringify({ action: 'end_round' }));
      
      setTimeout(() => {
        if (currentRoundRef.current >= maxRoundsRef.current) {
          setGameState('game_over');
        } else {
          setGameState('lobby');
        }
      }, 5000);
    }
  }, [gameState, timeLeft, ws]);

  const startGame = () => {
    setTimeLeft(60); 
    setCurrentRound((prev) => prev + 1); 
    
    const playerNames = players.map(p => p.name);
    ws.send(JSON.stringify({ 
      action: 'start_game', 
      players: playerNames 
    }));
  };

  const playAgain = () => {
    setCurrentRound(0); 
    setPlayers((prev) => prev.map(p => ({ ...p, score: 0 }))); 
    setGameState('lobby');
  };

  const sortedPlayers = [...players].sort((a, b) => b.score - a.score);

  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center p-8 font-sans relative">
      
      {gameState === 'lobby' && (
        <div className="flex flex-col items-center w-full max-w-5xl mt-8">
          <h1 className="text-6xl font-black mb-6 text-pink-500 tracking-wider">I'M NOT GONNA SAY NO NAMES</h1>
          
          <div className="flex flex-col items-center mb-10 bg-gray-800 px-8 py-4 rounded-2xl border-2 border-gray-700">
            <h3 className="text-2xl font-bold mb-4 text-gray-300">SELECT GAME LENGTH:</h3>
            <div className="flex gap-4">
              {[5, 10, 15].map(num => (
                <button key={num} onClick={() => setMaxRounds(num)} className={`px-8 py-3 rounded-full text-2xl font-bold transition-all border-4 ${maxRounds === num ? 'bg-pink-500 border-pink-400 text-white shadow-[0_0_20px_rgba(236,72,153,0.8)]' : 'bg-gray-900 border-gray-600 text-gray-400 hover:border-pink-400 hover:text-white'}`}>
                  {num} ROUNDS
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex w-full justify-between gap-12">
            <div className="flex flex-col items-center justify-center bg-gray-800 w-1/2 p-10 rounded-2xl border-4 border-blue-500 shadow-2xl">
              <h2 className="text-3xl mb-4 font-bold">JOIN AT: <span className="text-blue-400">NONAMES.LIVE</span></h2>
              <p className="text-2xl text-gray-400 mt-4">ROOM CODE</p>
              <p className="text-8xl font-black tracking-widest text-yellow-400 my-4">{roomCode}</p>
            </div>
            <div className="flex flex-col bg-gray-800 w-1/2 p-10 rounded-2xl border-4 border-pink-500 shadow-2xl">
              <h2 className="text-4xl font-bold mb-8 text-center text-pink-400">PLAYERS ({players.length})</h2>
              <div className="grid grid-cols-2 gap-4">
                {players.length === 0 && <p className="text-gray-400 italic col-span-2 text-center text-xl mt-10">Waiting for players...</p>}
                {players.map((player, idx) => (
                  <div key={idx} className="bg-gray-700 p-4 rounded-xl text-3xl font-bold text-center border-b-4 border-gray-600">
                    {player.name} - <span className="text-green-400">{player.score} pts</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <button onClick={startGame} disabled={players.length === 0} className={`mt-12 text-4xl font-bold py-6 px-16 rounded-full transition-all shadow-[0_0_30px_rgba(59,130,246,0.4)] ${players.length > 0 ? 'bg-blue-600 hover:bg-blue-500 text-white hover:scale-105' : 'bg-gray-600 text-gray-400'}`}>
            START ROUND {currentRound + 1}
          </button>
        </div>
      )}

      {gameState === 'actor_prep' && (
        <div className="flex flex-col items-center justify-center h-full mt-32 relative w-full">
          <div className="absolute top-0 left-0 bg-gray-800 border-2 border-gray-600 px-6 py-2 rounded-xl">
            <p className="text-2xl font-bold text-gray-300">ROUND {currentRound} OF {maxRounds}</p>
          </div>
          <h2 className="text-6xl font-black text-pink-400 mb-12 tracking-wide text-center animate-pulse">
            WAITING FOR {currentActor.toUpperCase()} TO START...
          </h2>
          <div className="text-[12rem] font-black text-gray-600 drop-shadow-md">60</div>
        </div>
      )}

      {gameState === 'active_turn' && (
        <div className="flex flex-col items-center justify-center h-full mt-32 relative w-full">
          <div className="absolute top-0 left-0 bg-gray-800 border-2 border-gray-600 px-6 py-2 rounded-xl">
            <p className="text-2xl font-bold text-gray-300">ROUND {currentRound} OF {maxRounds}</p>
          </div>
          <h2 className="text-8xl font-black text-yellow-400 mb-12 tracking-wide text-center">
            {currentActor.toUpperCase()} IS ACTING!
          </h2>
          <div className={`text-[12rem] font-black transition-colors duration-300 ${timeLeft <= 10 ? 'text-red-500 animate-ping drop-shadow-[0_0_40px_rgba(239,68,68,1)]' : 'text-pink-500 drop-shadow-[0_0_40px_rgba(236,72,153,0.8)]'}`}>
            {timeLeft}
          </div>
        </div>
      )}

      {gameState === 'round_over' && (
        <div className="flex flex-col items-center justify-center h-full mt-40 text-center">
          {celebrationMsg ? (
            <h2 className="text-[6rem] font-black text-green-500 mb-8 uppercase animate-bounce">{celebrationMsg}</h2>
          ) : (
            <h2 className="text-[10rem] font-black text-red-600 mb-8 uppercase animate-pulse">TIME IS UP!</h2>
          )}
          <p className="text-4xl text-gray-300 mt-8">{currentRound >= maxRounds ? "Tallying final scores..." : "Returning to lobby..."}</p>
        </div>
      )}

      {gameState === 'game_over' && (
        <div className="flex flex-col items-center justify-center h-full mt-20 w-full max-w-4xl">
          <h2 className="text-[7rem] font-black text-yellow-400 mb-12 tracking-wider drop-shadow-[0_0_40px_rgba(250,204,21,0.6)] animate-pulse">GAME OVER</h2>
          <div className="bg-gray-800 w-full p-10 rounded-3xl border-4 border-pink-500 shadow-2xl flex flex-col items-center">
            <h3 className="text-4xl font-bold mb-8 text-gray-300">FINAL STANDINGS</h3>
            <div className="flex flex-col w-full gap-4">
              {sortedPlayers.map((player, idx) => (
                <div key={idx} className={`flex justify-between items-center p-6 rounded-2xl border-4 ${idx === 0 ? 'bg-yellow-500/20 border-yellow-500 text-yellow-400 transform scale-105' : idx === 1 ? 'bg-gray-300/10 border-gray-400 text-gray-300' : idx === 2 ? 'bg-orange-700/20 border-orange-700 text-orange-500' : 'bg-gray-700 border-gray-600 text-gray-400'}`}>
                  <div className="flex items-center gap-6"><span className="text-5xl font-black">#{idx + 1}</span><span className="text-4xl font-bold">{player.name}</span></div>
                  <span className="text-4xl font-black">{player.score} PTS</span>
                </div>
              ))}
            </div>
          </div>
          <button onClick={playAgain} className="mt-12 text-4xl font-bold py-6 px-16 rounded-full bg-blue-600 hover:bg-blue-500 text-white transition-all hover:scale-105 shadow-[0_0_30px_rgba(59,130,246,0.4)]">PLAY AGAIN</button>
        </div>
      )}
    </div>
  );
};

export default HostScreen;