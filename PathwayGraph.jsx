// PathwayGraph.jsx
import ReactFlow, { Background, Controls, MiniMap } from 'reactflow';
import 'reactflow/dist/style.css';

const difficultyColor = {
  beginner: '#1D9E75',    // teal
  intermediate: '#BA7517', // amber
  advanced: '#7F77DD',    // purple
};

function CourseCard({ data }) {
  return (
    <div style={{
      background: 'var(--bg-surface)',
      border: `1.5px solid ${difficultyColor[data.difficulty]}`,
      borderRadius: 10,
      padding: '10px 14px',
      minWidth: 200,
      maxWidth: 240,
    }}>
      <div style={{ fontSize: 12, color: difficultyColor[data.difficulty], fontWeight: 500 }}>
        {data.difficulty.toUpperCase()} · {data.duration_hours}h
      </div>
      <div style={{ fontSize: 14, fontWeight: 500, marginTop: 4 }}>{data.title}</div>
      <div style={{ fontSize: 11, color: '#888', marginTop: 4 }}>
        {data.skills_covered.slice(0, 3).join(', ')}
        {data.skills_covered.length > 3 ? ` +${data.skills_covered.length - 3}` : ''}
      </div>
    </div>
  );
}

const nodeTypes = { courseCard: CourseCard };

export default function PathwayGraph({ courses }) {
  // Auto-layout: position nodes in columns by difficulty
  const nodes = courses.map((course, i) => ({
    id: course.id,
    type: 'courseCard',
    position: { x: (i % 3) * 280 + 40, y: Math.floor(i / 3) * 160 + 40 },
    data: course,
  }));

  const edges = courses.flatMap(course =>
    course.prerequisites.map(prereqId => ({
      id: `${prereqId}->${course.id}`,
      source: prereqId,
      target: course.id,
      animated: true,
      style: { stroke: '#7F77DD', strokeWidth: 1.5 },
    }))
  );

  return (
    <div style={{ height: 500, borderRadius: 12, overflow: 'hidden', border: '1px solid var(--border)' }}>
      <ReactFlow nodes={nodes} edges={edges} nodeTypes={nodeTypes} fitView>
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}