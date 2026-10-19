import React, { useState, useEffect, useRef } from 'react';
import QRCode from 'react-qr-code'; // <-- NEW: Imported the QR Code generator!

const HostScreen = () => {
  const [roomCode, setRoomCode] = useState('KJDS'); 
  const [players, setPlayers] = useState([]);
  
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
    const wsUrl = window.location.hostname === 'localhost' 
      ? `ws://localhost:8000/ws/${roomCode}/HOST`
      : `wss://nonames-game.onrender.com/ws/${roomCode}/HOST`;

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

  // The actual URL your friends will visit to join
  const joinUrl = "https://nonames-game.vercel.app";

  return (
    <div className="h-screen w-screen overflow-hidden bg-gray-900 text-white flex flex-col items-center p-4 lg:p-8 font-sans relative">
      
      {/* 1. LOBBY STATE */}
      {gameState === 'lobby' && (
        <div className="flex flex-col items-center justify-center w-full max-w-6xl h-full">
          <h1 className="text-5xl lg:text-6xl font-black mb-6 text-pink-500 tracking-wider text-center">
            I'M NOT GONNA SAY NO NAMES
          </h1>
          
          <div className="flex flex-col items-center mb-6 bg-gray-800 px-6 py-3 rounded-2xl border-2 border-gray-700">
            <h3 className="text-xl font-bold mb-3 text-gray-300">SELECT GAME LENGTH:</h3>
            <div className="flex gap-4">
              {[5, 10, 15].map(num => (
                <button key={num} onClick={() => setMaxRounds(num)} className={`px-6 py-2 rounded-full text-xl font-bold transition-all border-4 ${maxRounds === num ? 'bg-pink-500 border-pink-400 text-white shadow-[0_0_20px_rgba(236,72,153,0.8)]' : 'bg-gray-900 border-gray-600 text-gray-400 hover:border-pink-400 hover:text-white'}`}>
                  {num} ROUNDS
                </button>
              ))}
            </div>
          </div>
          
          <div className="flex w-full justify-between gap-8 h-3/5">
            {/* --- NEW: QR CODE SECTION --- */}
            <div className="flex flex-col items-center justify-center bg-gray-800 w-1/2 p-6 rounded-2xl border-4 border-blue-500 shadow-2xl h-full">
              <h2 className="text-2xl lg:text-3xl font-bold mb-4 text-gray-200">SCAN TO JOIN</h2>
              
              <div className="bg-white p-4 rounded-xl shadow-inner border-4 border-gray-300">
                <QRCode value={joinUrl} size={180} />
              </div>
              
              <p className="text-lg text-gray-400 mt-6">ENTER ROOM CODE:</p>
              <p className="text-6xl lg:text-7xl font-black tracking-widest text-yellow-400 mt-2">{roomCode}</p>
            </div>

            <div className="flex flex-col bg-gray-800 w-1/2 p-6 rounded-2xl border-4 border-pink-500 shadow-2xl h-full overflow-hidden">
              <h2 className="text-3xl font-bold mb-4 text-center text-pink-400">PLAYERS ({players.length})</h2>
              <div className="grid grid-cols-2 gap-3 overflow-y-auto pr-2 pb-2">
                {players.length === 0 && <p className="text-gray-400 italic col-span-2 text-center text-lg mt-4">Waiting for players...</p>}
                {players.map((player, idx) => (
                  <div key={idx} className="bg-gray-700 p-3 rounded-xl text-2xl font-bold text-center border-b-4 border-gray-600 truncate">
                    {player.name} - <span className="text-green-400">{player.score}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <button onClick={startGame} disabled={players.length === 0} className={`mt-8 text-3xl font-bold py-4 px-12 rounded-full transition-all shadow-[0_0_30px_rgba(59,130,246,0.4)] ${players.length > 0 ? 'bg-blue-600 hover:bg-blue-500 text-white hover:scale-105' : 'bg-gray-600 text-gray-400'}`}>
            START ROUND {currentRound + 1}
          </button>
        </div>
      )}

      {/* ACTOR PREP STATE */}
      {gameState === 'actor_prep' && (
        <div className="flex flex-col items-center justify-center h-full relative w-full">
          <div className="absolute top-4 left-4 lg:top-8 lg:left-8 bg-gray-800 border-2 border-gray-600 px-6 py-2 rounded-xl">
            <p className="text-2xl font-bold text-gray-300">ROUND {currentRound} OF {maxRounds}</p>
          </div>
          <h2 className="text-5xl lg:text-7xl font-black text-pink-400 mb-8 tracking-wide text-center animate-pulse">
            WAITING FOR {currentActor.toUpperCase()} TO START...
          </h2>
          <div className="text-[10rem] lg:text-[14rem] font-black text-gray-600 drop-shadow-md leading-none">60</div>
        </div>
      )}

      {/* ACTIVE TURN STATE */}
      {gameState === 'active_turn' && (
        <div className="flex flex-col items-center justify-center h-full relative w-full">
          <div className="absolute top-4 left-4 lg:top-8 lg:left-8 bg-gray-800 border-2 border-gray-600 px-6 py-2 rounded-xl">
            <p className="text-2xl font-bold text-gray-300">ROUND {currentRound} OF {maxRounds}</p>
          </div>
          <h2 className="text-6xl lg:text-8xl font-black text-yellow-400 mb-8 tracking-wide text-center leading-none">
            {currentActor.toUpperCase()} IS ACTING!
          </h2>
          <div className={`text-[12rem] lg:text-[16rem] font-black transition-colors duration-300 leading-none ${timeLeft <= 10 ? 'text-red-500 animate-ping drop-shadow-[0_0_40px_rgba(239,68,68,1)]' : 'text-pink-500 drop-shadow-[0_0_40px_rgba(236,72,153,0.8)]'}`}>
            {timeLeft}
          </div>
        </div>
      )}

      {/* ROUND OVER STATE */}
      {gameState === 'round_over' && (
        <div className="flex flex-col items-center justify-center h-full text-center">
          {celebrationMsg ? (
            <h2 className="text-[5rem] lg:text-[7rem] font-black text-green-500 mb-6 uppercase animate-bounce leading-none drop-shadow-lg">{celebrationMsg}</h2>
          ) : (
            <h2 className="text-[8rem] lg:text-[12rem] font-black text-red-600 mb-6 uppercase animate-pulse leading-none drop-shadow-[0_0_50px_rgba(220,38,38,1)]">TIME IS UP!</h2>
          )}
          <p className="text-3xl lg:text-5xl text-gray-300">{currentRound >= maxRounds ? "Tallying final scores..." : "Returning to lobby..."}</p>
        </div>
      )}

      {/* GAME OVER SCOREBOARD */}
      {gameState === 'game_over' && (
        <div className="flex flex-col items-center justify-center h-full w-full max-w-4xl">
          <h2 className="text-[5rem] lg:text-[7rem] font-black text-yellow-400 mb-8 tracking-wider drop-shadow-[0_0_40px_rgba(250,204,21,0.6)] animate-pulse leading-none">GAME OVER</h2>
          <div className="bg-gray-800 w-full p-8 rounded-3xl border-4 border-pink-500 shadow-2xl flex flex-col items-center max-h-[50vh] overflow-hidden">
            <h3 className="text-3xl font-bold mb-6 text-gray-300">FINAL STANDINGS</h3>
            <div className="flex flex-col w-full gap-3 overflow-y-auto pr-2 pb-2">
              {sortedPlayers.map((player, idx) => (
                <div key={idx} className={`flex justify-between items-center p-4 lg:p-6 rounded-2xl border-4 ${idx === 0 ? 'bg-yellow-500/20 border-yellow-500 text-yellow-400 transform scale-105' : idx === 1 ? 'bg-gray-300/10 border-gray-400 text-gray-300' : idx === 2 ? 'bg-orange-700/20 border-orange-700 text-orange-500' : 'bg-gray-700 border-gray-600 text-gray-400'}`}>
                  <div className="flex items-center gap-4 lg:gap-6"><span className="text-4xl lg:text-5xl font-black">#{idx + 1}</span><span className="text-3xl lg:text-4xl font-bold truncate">{player.name}</span></div>
                  <span className="text-3xl lg:text-4xl font-black">{player.score} PTS</span>
                </div>
              ))}
            </div>
          </div>
          <button onClick={playAgain} className="mt-8 text-3xl lg:text-4xl font-bold py-5 px-12 rounded-full bg-blue-600 hover:bg-blue-500 text-white transition-all hover:scale-105 shadow-[0_0_30px_rgba(59,130,246,0.4)]">PLAY AGAIN</button>
        </div>
      )}
    </div>
  );
};

export default HostScreen;