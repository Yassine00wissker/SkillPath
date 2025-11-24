const ResultList = ({ results }) => {
  if (!results || (!results.jobs?.length && !results.formations?.length)) {
    return (
      <div className="text-center text-gray-500 py-8">
        No recommendations available
      </div>
    );
  }

  const handleSave = (item, type) => {
    // For now, just store locally
    const saved = JSON.parse(localStorage.getItem('savedItems') || '[]');
    saved.push({ ...item, type, savedAt: new Date().toISOString() });
    localStorage.setItem('savedItems', JSON.stringify(saved));
    alert(`${type === 'job' ? 'Job' : 'Formation'} saved!`);
  };

  return (
    <div className="space-y-8">
      {/* Jobs Section */}
      {results.jobs && results.jobs.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Recommended Jobs</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.jobs.map((job) => (
              <div
                key={job.id || job.title}
                className="bg-white rounded-lg shadow-md p-6 relative hover:shadow-lg transition-shadow"
              >
                <div className="absolute top-4 right-4">
                  <span className="bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {typeof job.score === 'number' ? job.score.toFixed(2) : job.score}
                  </span>
                </div>
                <h3 className="text-xl font-semibold mb-2 pr-16">{job.title}</h3>
                {job.description && (
                  <p className="text-gray-600 text-sm mb-3">{job.description}</p>
                )}
                {job.requirements && (
                  <div className="flex flex-wrap gap-2 mb-3">
                    {job.requirements.map((req, idx) => (
                      <span
                        key={idx}
                        className="bg-gray-100 text-gray-700 text-xs px-2 py-1 rounded"
                      >
                        {req}
                      </span>
                    ))}
                  </div>
                )}
                {job.explanation && (
                  <p className="text-sm text-gray-500 italic mb-3">{job.explanation}</p>
                )}
                <button
                  onClick={() => handleSave(job, 'job')}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded transition-colors"
                >
                  Save
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Formations Section */}
      {results.formations && results.formations.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold mb-4">Recommended Formations</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {results.formations.map((formation) => (
              <div
                key={formation.id}
                className="bg-white rounded-lg shadow-md p-6 relative hover:shadow-lg transition-shadow"
              >
                <div className="absolute top-4 right-4">
                  <span className="bg-purple-100 text-purple-800 text-xs font-semibold px-2.5 py-0.5 rounded">
                    {typeof formation.score === 'number' ? formation.score.toFixed(2) : formation.score}
                  </span>
                </div>
                <h3 className="text-xl font-semibold mb-2 pr-16">{formation.title}</h3>
                {formation.description && (
                  <p className="text-gray-600 text-sm mb-3">{formation.description}</p>
                )}
                {formation.explanation && (
                  <p className="text-sm text-gray-500 italic mb-3">{formation.explanation}</p>
                )}
                <button
                  onClick={() => handleSave(formation, 'formation')}
                  className="w-full bg-green-600 hover:bg-green-700 text-white py-2 px-4 rounded transition-colors"
                >
                  Save
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {results.source && (
        <div className="text-center text-sm text-gray-500">
          Source: {results.source}
          {results.fallback_reason && (
            <span className="block text-orange-600 mt-1">
              Fallback reason: {results.fallback_reason}
            </span>
          )}
        </div>
      )}
    </div>
  );
};

export default ResultList;

