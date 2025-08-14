import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BookOpenIcon, ClockIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface VocabularyWord {
  id: number;
  word: string;
  translation: string;
  part_of_speech: string;
  difficulty: string;
  example_sentence: string;
  pronunciation: string;
  next_review: string;
  interval: number;
  ease_factor: number;
}

const Vocabulary: React.FC = () => {
  const [words, setWords] = useState<VocabularyWord[]>([]);
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Mock data for demonstration
  useEffect(() => {
    const mockWords: VocabularyWord[] = [
      {
        id: 1,
        word: 'ciao',
        translation: 'hello/hi',
        part_of_speech: 'interjection',
        difficulty: 'beginner',
        example_sentence: 'Ciao! Come stai?',
        pronunciation: 'chow',
        next_review: '2024-01-15',
        interval: 1,
        ease_factor: 2.5
      },
      {
        id: 2,
        word: 'grazie',
        translation: 'thank you',
        part_of_speech: 'interjection',
        difficulty: 'beginner',
        example_sentence: 'Grazie mille per l\'aiuto!',
        pronunciation: 'grah-tsee-eh',
        next_review: '2024-01-16',
        interval: 1,
        ease_factor: 2.5
      },
      {
        id: 3,
        word: 'acqua',
        translation: 'water',
        part_of_speech: 'noun',
        difficulty: 'beginner',
        example_sentence: 'Vorrei un bicchiere d\'acqua.',
        pronunciation: 'ah-kwah',
        next_review: '2024-01-17',
        interval: 1,
        ease_factor: 2.5
      }
    ];
    
    setWords(mockWords);
    setIsLoading(false);
  }, []);

  const handleShowAnswer = () => {
    setShowAnswer(true);
  };

  const handleResponse = (quality: number) => {
    const currentWord = words[currentWordIndex];
    
    // Simulate spaced repetition algorithm
    let newInterval: number;
    let newEaseFactor: number;
    
    if (quality >= 3) {
      // Good response
      newInterval = currentWord.interval * 2;
      newEaseFactor = Math.max(1.3, currentWord.ease_factor + 0.1);
      toast.success(`Great job! You'll see "${currentWord.word}" again in ${newInterval} days.`);
    } else {
      // Poor response
      newInterval = 1;
      newEaseFactor = Math.max(1.3, currentWord.ease_factor - 0.2);
      toast.error(`Keep practicing! You'll see "${currentWord.word}" again tomorrow.`);
    }

    // Update word data
    const updatedWords = words.map((word, index) => 
      index === currentWordIndex 
        ? { ...word, interval: newInterval, ease_factor: newEaseFactor }
        : word
    );
    
    setWords(updatedWords);
    
    // Move to next word or reset
    if (currentWordIndex < words.length - 1) {
      setCurrentWordIndex(currentWordIndex + 1);
    } else {
      setCurrentWordIndex(0);
      toast.success('Session complete! Great work! 🎉');
    }
    
    setShowAnswer(false);
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const currentWord = words[currentWordIndex];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Vocabulary Practice 🇮🇹</h1>
        <p className="text-gray-600">Learn and review Italian words with spaced repetition</p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            Word {currentWordIndex + 1} of {words.length}
          </span>
          <span className="text-sm text-gray-500">
            {Math.round(((currentWordIndex + 1) / words.length) * 100)}% Complete
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className="bg-blue-600 h-2 rounded-full"
            initial={{ width: 0 }}
            animate={{ width: `${((currentWordIndex + 1) / words.length) * 100}%` }}
            transition={{ duration: 0.5 }}
          />
        </div>
      </div>

      {/* Word Card */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        <div className="text-center mb-6">
          <h2 className="text-4xl font-bold text-gray-900 mb-2">{currentWord.word}</h2>
          <p className="text-lg text-gray-600 mb-4">Pronunciation: {currentWord.pronunciation}</p>
          <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
            <BookOpenIcon className="w-4 h-4 mr-2" />
            {currentWord.difficulty}
          </div>
        </div>

        {!showAnswer ? (
          <div className="text-center">
            <p className="text-gray-600 mb-6">What does this word mean?</p>
            <button
              onClick={handleShowAnswer}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Show Answer
            </button>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="text-center">
              <h3 className="text-2xl font-semibold text-gray-900 mb-2">
                {currentWord.translation}
              </h3>
              <p className="text-gray-600 mb-4">
                <span className="font-medium">Part of speech:</span> {currentWord.part_of_speech}
              </p>
              <p className="text-gray-700 italic mb-4">"{currentWord.example_sentence}"</p>
            </div>

            {/* Response Buttons */}
            <div className="grid grid-cols-5 gap-3">
              <button
                onClick={() => handleResponse(1)}
                className="flex flex-col items-center p-3 rounded-lg border-2 border-red-200 hover:border-red-300 hover:bg-red-50 transition-colors"
              >
                <XCircleIcon className="w-6 h-6 text-red-500 mb-1" />
                <span className="text-xs text-red-600">Again</span>
              </button>
              <button
                onClick={() => handleResponse(2)}
                className="flex flex-col items-center p-3 rounded-lg border-2 border-orange-200 hover:border-orange-300 hover:bg-orange-50 transition-colors"
              >
                <span className="text-lg text-orange-500 mb-1">😕</span>
                <span className="text-xs text-orange-600">Hard</span>
              </button>
              <button
                onClick={() => handleResponse(3)}
                className="flex flex-col items-center p-3 rounded-lg border-2 border-yellow-200 hover:border-yellow-300 hover:bg-yellow-50 transition-colors"
              >
                <span className="text-lg text-yellow-500 mb-1">😐</span>
                <span className="text-xs text-yellow-600">Good</span>
              </button>
              <button
                onClick={() => handleResponse(4)}
                className="flex flex-col items-center p-3 rounded-lg border-2 border-green-200 hover:border-green-300 hover:bg-green-50 transition-colors"
              >
                <span className="text-lg text-green-500 mb-1">😊</span>
                <span className="text-xs text-green-600">Easy</span>
              </button>
              <button
                onClick={() => handleResponse(5)}
                className="flex flex-col items-center p-3 rounded-lg border-2 border-blue-200 hover:border-blue-300 hover:bg-blue-50 transition-colors"
              >
                <CheckCircleIcon className="w-6 h-6 text-blue-500 mb-1" />
                <span className="text-xs text-blue-600">Perfect</span>
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <ClockIcon className="w-8 h-8 text-blue-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Next Review</p>
              <p className="text-lg font-semibold text-gray-900">
                {new Date(currentWord.next_review).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <BookOpenIcon className="w-8 h-8 text-green-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Interval</p>
              <p className="text-lg font-semibold text-gray-900">
                {currentWord.interval} day{currentWord.interval !== 1 ? 's' : ''}
              </p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <CheckCircleIcon className="w-8 h-8 text-purple-500 mr-3" />
            <div>
              <p className="text-sm font-medium text-gray-600">Ease Factor</p>
              <p className="text-lg font-semibold text-gray-900">
                {currentWord.ease_factor.toFixed(1)}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Vocabulary;
