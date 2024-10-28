// src/components/SearchInput.tsx
import React, { useState } from 'react';

const SearchInput: React.FC = () => {
  const [query, setQuery] = useState('');
  const [entity, setEntity] = useState<'thermometers' | 'users' | 'categories' | 'properties'>('thermometers');
  const [results, setResults] = useState<any[]>([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/${entity}/search?query=${encodeURIComponent(query)}`);
      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        console.error('Error fetching search results');
      }
    } catch (error) {
      console.error('Error fetching search results:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="flex items-center space-x-4 mb-4">
        <select
          value={entity}
          onChange={(e) => setEntity(e.target.value as any)}
          className="px-4 py-2 border border-gray-300 rounded"
        >
          <option value="thermometers">Thermometers</option>
          <option value="users">Users</option>
          <option value="categories">Categories</option>
          <option value="properties">Properties</option>
        </select>

        <input
          type="text"
          placeholder="Search..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded w-full"
        />

        <button
          onClick={handleSearch}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          Search
        </button>
      </div>

      <div>
        <h2 className="text-lg font-semibold mb-2">Results:</h2>
        {results.length === 0 ? (
          <p>No results found</p>
        ) : (
          <table className="min-w-full divide-y divide-gray-200">
            <thead>
              <tr>
                {results[0] && Object.keys(results[0]).map((key) => (
                  <th key={key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {key}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {results.map((item) => (
                <tr key={item.id}>
                  {Object.values(item).map((value, index) => (
                    <td key={index} className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {/* eslint-disable-next-line @typescript-eslint/ban-ts-comment */}
                      {/*@ts-expect-error  */}
                      {value}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default SearchInput;
