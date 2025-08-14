import React from 'react';
import { motion } from 'framer-motion';
import { 
  BookOpenIcon, 
  ClockIcon, 
  StarIcon, 
  TrophyIcon,
  TrendingUpIcon,
  CalendarIcon
} from '@heroicons/react/24/outline';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const Progress: React.FC = () => {
  const weeklyData = [
    { day: 'Mon', words: 5, reviews: 12 },
    { day: 'Tue', words: 8, reviews: 15 },
    { day: 'Wed', words: 6, reviews: 10 },
    { day: 'Thu', words: 10, reviews: 18 },
    { day: 'Fri', words: 7, reviews: 14 },
    { day: 'Sat', words: 12, reviews: 20 },
    { day: 'Sun', words: 9, reviews: 16 }
  ];

  const masteryData = [
    { name: 'New', value: 25, color: '#6B7280' },
    { name: 'Learning', value: 40, color: '#3B82F6' },
    { name: 'Reviewing', value: 20, color: '#F59E0B' },
    { name: 'Mastered', value: 15, color: '#10B981' }
  ];

  const achievements = [
    { title: 'First Steps', description: 'Learned your first 10 words', icon: '🎯', unlocked: true },
    { title: 'Week Warrior', description: '7-day learning streak', icon: '🔥', unlocked: true },
    { title: 'Vocabulary Master', description: '100 words learned', icon: '📚', unlocked: false },
    { title: 'Consistency King', description: '30-day learning streak', icon: '👑', unlocked: false }
  ];

  return (
    <div className="max-w-7xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Learning Progress 📊</h1>
        <p className="text-gray-600">Track your Italian language learning journey</p>
      </div>

      {/* Summary Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-blue-100 rounded-lg">
              <BookOpenIcon className="w-6 h-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Total Words</p>
              <p className="text-2xl font-bold text-gray-900">150</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-green-100 rounded-lg">
              <StarIcon className="w-6 h-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Words Learned</p>
              <p className="text-2xl font-bold text-gray-900">87</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-purple-100 rounded-lg">
              <TrendingUpIcon className="w-6 h-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Accuracy</p>
              <p className="text-2xl font-bold text-gray-900">78%</p>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <div className="flex items-center">
            <div className="p-3 bg-orange-100 rounded-lg">
              <ClockIcon className="w-6 h-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">Study Time</p>
              <p className="text-2xl font-bold text-gray-900">45h</p>
            </div>
          </div>
        </motion.div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Activity</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={weeklyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="day" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="words" fill="#3B82F6" name="New Words" />
              <Bar dataKey="reviews" fill="#10B981" name="Reviews" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-lg shadow p-6"
        >
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Mastery Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={masteryData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {masteryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      {/* Achievements */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="bg-white rounded-lg shadow p-6 mb-8"
      >
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Achievements</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {achievements.map((achievement, index) => (
            <div
              key={achievement.title}
              className={`p-4 rounded-lg border-2 ${
                achievement.unlocked
                  ? 'border-green-200 bg-green-50'
                  : 'border-gray-200 bg-gray-50'
              }`}
            >
              <div className="flex items-center">
                <span className="text-2xl mr-3">{achievement.icon}</span>
                <div>
                  <h4 className={`font-medium ${
                    achievement.unlocked ? 'text-green-800' : 'text-gray-600'
                  }`}>
                    {achievement.title}
                  </h4>
                  <p className={`text-sm ${
                    achievement.unlocked ? 'text-green-600' : 'text-gray-500'
                  }`}>
                    {achievement.description}
                  </p>
                </div>
                {achievement.unlocked && (
                  <TrophyIcon className="w-5 h-5 text-green-600 ml-auto" />
                )}
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Learning Streak */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-8 text-white text-center"
      >
        <div className="flex items-center justify-center mb-4">
          <CalendarIcon className="w-8 h-8 mr-3" />
          <h3 className="text-2xl font-bold">Learning Streak</h3>
        </div>
        <div className="text-6xl font-bold mb-4">12</div>
        <p className="text-xl mb-4">days in a row!</p>
        <p className="text-blue-100">
          Keep up the amazing work! Consistency is the key to language learning success.
        </p>
      </motion.div>
    </div>
  );
};

export default Progress;
