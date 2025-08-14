import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  BookOpenIcon, 
  ChatBubbleLeftRightIcon, 
  ChartBarIcon, 
  AcademicCapIcon,
  ClockIcon,
  StarIcon,
  FireIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

interface LearningStats {
  totalWords: number;
  wordsLearned: number;
  currentStreak: number;
  longestStreak: number;
  accuracy: number;
  timeSpent: number;
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<LearningStats>({
    totalWords: 150,
    wordsLearned: 87,
    currentStreak: 12,
    longestStreak: 23,
    accuracy: 78,
    timeSpent: 45
  });

  const [recentActivity, setRecentActivity] = useState([
    { id: 1, word: 'ciao', action: 'learned', time: '2 hours ago' },
    { id: 2, word: 'grazie', action: 'reviewed', time: '1 day ago' },
    { id: 3, word: 'acqua', action: 'mastered', time: '2 days ago' },
    { id: 4, word: 'essere', action: 'practiced', time: '3 days ago' }
  ]);

  const [chartData, setChartData] = useState([
    { day: 'Mon', words: 5, accuracy: 80 },
    { day: 'Tue', words: 8, accuracy: 75 },
    { day: 'Wed', words: 6, accuracy: 85 },
    { day: 'Thu', words: 10, accuracy: 90 },
    { day: 'Fri', words: 7, accuracy: 82 },
    { day: 'Sat', words: 12, accuracy: 88 },
    { day: 'Sun', words: 9, accuracy: 85 }
  ]);

  const quickActions = [
    {
      title: 'Practice Vocabulary',
      description: 'Review words with spaced repetition',
      icon: BookOpenIcon,
      color: 'bg-blue-500',
      link: '/vocabulary'
    },
    {
      title: 'AI Conversation',
      description: 'Chat with your Italian tutor',
      icon: ChatBubbleLeftRightIcon,
      color: 'bg-green-500',
      link: '/conversation'
    },
    {
      title: 'View Progress',
      description: 'Track your learning journey',
      icon: ChartBarIcon,
      color: 'bg-purple-500',
      link: '/progress'
    }
  ];

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Welcome Header */}
      <div className="mb-8">
        <motion.h1 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-4xl font-bold text-gray-900 mb-2"
        >
          Benvenuto! 🇮🇹 Welcome back!
        </motion.h1>
        <p className="text-xl text-gray-600">
          Ready to continue your Italian learning journey?
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <BookOpenIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Words Learned</p>
              <p className="text-2xl font-bold text-gray-900">{stats.wordsLearned}</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <FireIcon className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Current Streak</p>
              <p className="text-2xl font-bold text-gray-900">{stats.currentStreak} days</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <StarIcon className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">{stats.accuracy}%</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <ClockIcon className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Time Spent</p>
              <p className="text-2xl font-bold text-gray-900">{stats.timeSpent}h</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action, index) => (
            <motion.div
              key={action.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 * index }}
              whileHover={{ scale: 1.02 }}
              className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow cursor-pointer"
            >
              <Link to={action.link} className="block">
                <div className="flex items-center mb-4">
                  <div className={`p-3 rounded-lg ${action.color}`}>
                    <action.icon className="w-6 h-6 text-white" />
                  </div>
                  <h3 className="ml-3 text-lg font-semibold text-gray-900">{action.title}</h3>
                </div>
                <p className="text-gray-600">{action.description}</p>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Progress Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Progress</h3>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="words" stroke="#3B82F6" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <div className="space-y-3">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-blue-500 rounded-full mr-3"></div>
                  <span className="font-medium text-gray-900">{activity.word}</span>
                  <span className="text-gray-500 ml-2">({activity.action})</span>
                </div>
                <span className="text-sm text-gray-500">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Motivation Section */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-8 text-white text-center">
        <TrophyIcon className="w-16 h-16 mx-auto mb-4 text-yellow-300" />
        <h3 className="text-2xl font-bold mb-2">Keep Up the Great Work!</h3>
        <p className="text-blue-100 mb-4">
          You're on a {stats.currentStreak}-day streak! Consistency is the key to language learning success.
        </p>
        <div className="flex justify-center space-x-4">
          <Link
            to="/vocabulary"
            className="bg-white text-blue-600 px-6 py-2 rounded-lg font-medium hover:bg-gray-100 transition-colors"
          >
            Practice Now
          </Link>
          <Link
            to="/conversation"
            className="bg-transparent border-2 border-white text-white px-6 py-2 rounded-lg font-medium hover:bg-white hover:text-blue-600 transition-colors"
          >
            Start Chat
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 