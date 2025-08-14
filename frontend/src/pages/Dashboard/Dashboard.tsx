import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  AcademicCapIcon, 
  ChatBubbleLeftRightIcon, 
  ChartBarIcon,
  PlayIcon,
  ClockIcon,
  TrophyIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../../contexts/AuthContext';
import axios from 'axios';

interface LearningStats {
  total_words_learning: number;
  total_reviews: number;
  correct_reviews: number;
  accuracy_rate: number;
  words_due_review: number;
  mastery_distribution: Record<string, number>;
  average_ease_factor: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<LearningStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchLearningStats();
  }, []);

  const fetchLearningStats = async () => {
    try {
      const response = await axios.get('/api/v1/learning/statistics');
      setStats(response.data);
    } catch (error) {
      console.error('Failed to fetch learning stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getMasteryLevelName = (level: number): string => {
    const levels = {
      1: 'New',
      2: 'Beginner',
      3: 'Intermediate',
      4: 'Advanced',
      5: 'Mastered'
    };
    return levels[level as keyof typeof levels] || 'Unknown';
  };

  const getMasteryLevelColor = (level: number): string => {
    const colors = {
      1: 'bg-gray-100 text-gray-800',
      2: 'bg-blue-100 text-blue-800',
      3: 'bg-yellow-100 text-yellow-800',
      4: 'bg-orange-100 text-orange-800',
      5: 'bg-green-100 text-green-800'
    };
    return colors[level as keyof typeof colors] || 'bg-gray-100 text-gray-800';
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          ¡Hola, {user?.username}! 👋
        </h1>
        <p className="text-xl text-gray-600">
          Ready to continue your {user?.target_language?.toUpperCase()} learning journey?
        </p>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link
          to="/learn"
          className="card hover:shadow-soft transition-shadow duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors duration-200">
              <AcademicCapIcon className="h-8 w-8 text-blue-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Start Learning</h3>
              <p className="text-gray-600">Review words and learn new ones</p>
            </div>
            <PlayIcon className="h-5 w-5 text-gray-400 group-hover:text-blue-600 transition-colors duration-200" />
          </div>
        </Link>

        <Link
          to="/conversation"
          className="card hover:shadow-soft transition-shadow duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors duration-200">
              <ChatBubbleLeftRightIcon className="h-8 w-8 text-green-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">AI Conversation</h3>
              <p className="text-gray-600">Practice with your AI tutor</p>
            </div>
            <PlayIcon className="h-5 w-5 text-gray-400 group-hover:text-green-600 transition-colors duration-200" />
          </div>
        </Link>

        <Link
          to="/progress"
          className="card hover:shadow-soft transition-shadow duration-200 group"
        >
          <div className="flex items-center space-x-4">
            <div className="p-3 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors duration-200">
              <ChartBarIcon className="h-8 w-8 text-purple-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">View Progress</h3>
              <p className="text-gray-600">Track your learning journey</p>
            </div>
            <PlayIcon className="h-5 w-5 text-gray-400 group-hover:text-purple-600 transition-colors duration-200" />
          </div>
        </Link>
      </div>

      {/* Learning Statistics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card text-center">
            <div className="p-3 bg-blue-100 rounded-lg w-12 h-12 mx-auto mb-3 flex items-center justify-center">
              <AcademicCapIcon className="h-6 w-6 text-blue-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">{stats.total_words_learning}</h3>
            <p className="text-gray-600">Words Learning</p>
          </div>

          <div className="card text-center">
            <div className="p-3 bg-green-100 rounded-lg w-12 h-12 mx-auto mb-3 flex items-center justify-center">
              <ClockIcon className="h-6 w-6 text-green-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">{stats.words_due_review}</h3>
            <p className="text-gray-600">Due for Review</p>
          </div>

          <div className="card text-center">
            <div className="p-3 bg-yellow-100 rounded-lg w-12 h-12 mx-auto mb-3 flex items-center justify-center">
              <ChartBarIcon className="h-6 w-6 text-yellow-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">{stats.accuracy_rate}%</h3>
            <p className="text-gray-600">Accuracy Rate</p>
          </div>

          <div className="card text-center">
            <div className="p-3 bg-purple-100 rounded-lg w-12 h-12 mx-auto mb-3 flex items-center justify-center">
              <TrophyIcon className="h-6 w-6 text-purple-600" />
            </div>
            <h3 className="text-2xl font-bold text-gray-900">{stats.total_reviews}</h3>
            <p className="text-gray-600">Total Reviews</p>
          </div>
        </div>
      )}

      {/* Mastery Distribution */}
      {stats && stats.mastery_distribution && (
        <div className="card">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Mastery Distribution</h3>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {Object.entries(stats.mastery_distribution).map(([level, count]) => (
              <div key={level} className="text-center">
                <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getMasteryLevelColor(parseInt(level))}`}>
                  {getMasteryLevelName(parseInt(level))}
                </div>
                <p className="text-2xl font-bold text-gray-900 mt-2">{count}</p>
                <p className="text-xs text-gray-500">words</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Daily Goal Progress */}
      <div className="card">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Learning Goal</h3>
        <div className="bg-gray-100 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Daily Progress</span>
            <span className="text-sm font-medium text-gray-700">
              {stats?.total_reviews || 0} / 20 words
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-blue-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${Math.min((stats?.total_reviews || 0) / 20 * 100, 100)}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-600 mt-2">
            Keep going! You're making great progress with your spaced repetition learning.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard; 