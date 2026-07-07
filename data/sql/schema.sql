-- StadiumVerse AI - Complete Database Schema
-- FIFA World Cup 2026 Stadium Digital Twin System

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- Enums
CREATE TYPE user_role AS ENUM ('admin', 'operator', 'volunteer', 'fan');
CREATE TYPE fan_emotion AS ENUM ('excited', 'joyful', 'angry', 'stressed', 'confused', 'tired', 'fearful', 'neutral');
CREATE TYPE accessibility_need AS ENUM ('wheelchair', 'visual_impairment', 'hearing_impairment', 'mobility_aid', 'none');
CREATE TYPE transport_mode AS ENUM ('walking', 'metro', 'bus', 'taxi', 'car', 'bike');
CREATE TYPE emergency_type AS ENUM ('medical', 'security', 'fire', 'evacuation', 'crowd_crush', 'weather');
CREATE TYPE volunteer_skill AS ENUM ('first_aid', 'multilingual', 'crowd_control', 'technical', 'accessibility');
CREATE TYPE prediction_type AS ENUM ('movement', 'purchase', 'restroom', 'exit', 'emergency', 'queue');

-- Users and Authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role user_role NOT NULL DEFAULT 'fan',
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Stadium Layout
CREATE TABLE stadium_zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    zone_type VARCHAR(50) NOT NULL, -- gate, food_court, restroom, seating, medical, security
    capacity INTEGER,
    coordinates GEOMETRY(POLYGON, 4326),
    level INTEGER DEFAULT 1,
    accessibility_features TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stadium_facilities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID REFERENCES stadium_zones(id),
    facility_type VARCHAR(50) NOT NULL, -- gate, food_stand, restroom, medical_station, info_desk
    name VARCHAR(100) NOT NULL,
    location GEOMETRY(POINT, 4326) NOT NULL,
    capacity INTEGER,
    current_queue_length INTEGER DEFAULT 0,
    average_service_time INTEGER, -- seconds
    is_operational BOOLEAN DEFAULT true,
    accessibility_features TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Digital Fans (Core of the system)
CREATE TABLE digital_fans (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    fan_id VARCHAR(20) UNIQUE NOT NULL, -- F001, F002, etc.
    name VARCHAR(100) NOT NULL,
    country VARCHAR(3) NOT NULL, -- ISO country code
    language VARCHAR(10) NOT NULL,
    age INTEGER NOT NULL,
    accessibility_needs accessibility_need DEFAULT 'none',
    favorite_team VARCHAR(100),
    
    -- Current State
    current_emotion fan_emotion DEFAULT 'neutral',
    stress_level INTEGER CHECK (stress_level BETWEEN 0 AND 100) DEFAULT 50,
    excitement_level INTEGER CHECK (excitement_level BETWEEN 0 AND 100) DEFAULT 50,
    walking_speed DECIMAL(3,1) DEFAULT 1.2, -- m/s
    hunger_level INTEGER CHECK (hunger_level BETWEEN 0 AND 100) DEFAULT 30,
    fatigue_level INTEGER CHECK (fatigue_level BETWEEN 0 AND 100) DEFAULT 20,
    battery_level INTEGER CHECK (battery_level BETWEEN 0 AND 100) DEFAULT 80,
    
    -- Location and Movement
    current_location GEOMETRY(POINT, 4326) NOT NULL,
    destination GEOMETRY(POINT, 4326),
    transportation transport_mode DEFAULT 'walking',
    
    -- Behavioral Patterns
    purchase_intent INTEGER CHECK (purchase_intent BETWEEN 0 AND 100) DEFAULT 30,
    medical_risk_score INTEGER CHECK (medical_risk_score BETWEEN 0 AND 100) DEFAULT 10,
    lost_probability DECIMAL(3,2) CHECK (lost_probability BETWEEN 0.00 AND 1.00) DEFAULT 0.05,
    queue_tolerance INTEGER CHECK (queue_tolerance BETWEEN 0 AND 100) DEFAULT 60,
    risk_score INTEGER CHECK (risk_score BETWEEN 0 AND 100) DEFAULT 20,
    
    -- Predictions
    predicted_next_action TEXT,
    prediction_confidence DECIMAL(3,2) CHECK (prediction_confidence BETWEEN 0.00 AND 1.00),
    predicted_exit_time TIMESTAMP WITH TIME ZONE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Fan Movement History
CREATE TABLE fan_movements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fan_id UUID REFERENCES digital_fans(id),
    location GEOMETRY(POINT, 4326) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    speed DECIMAL(3,1),
    direction DECIMAL(5,2), -- degrees
    zone_id UUID REFERENCES stadium_zones(id)
);

-- Fan Predictions
CREATE TABLE fan_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fan_id UUID REFERENCES digital_fans(id),
    prediction_type prediction_type NOT NULL,
    predicted_location GEOMETRY(POINT, 4326),
    predicted_time TIMESTAMP WITH TIME ZONE NOT NULL,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0.00 AND 1.00),
    prediction_data JSONB, -- flexible storage for prediction details
    actual_outcome JSONB, -- for learning and validation
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    is_accurate BOOLEAN -- set after validation
);

-- Volunteers
CREATE TABLE volunteers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    volunteer_id VARCHAR(20) UNIQUE NOT NULL, -- V001, V002, etc.
    name VARCHAR(100) NOT NULL,
    languages TEXT[] NOT NULL DEFAULT ARRAY['en'],
    skills volunteer_skill[] DEFAULT ARRAY[]::volunteer_skill[],
    medical_training BOOLEAN DEFAULT false,
    current_location GEOMETRY(POINT, 4326),
    availability_status VARCHAR(20) DEFAULT 'available', -- available, busy, break, offline
    shift_start TIMESTAMP WITH TIME ZONE,
    shift_end TIMESTAMP WITH TIME ZONE,
    zone_assignment UUID REFERENCES stadium_zones(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true
);

-- Volunteer Tasks
CREATE TABLE volunteer_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    volunteer_id UUID REFERENCES volunteers(id),
    task_type VARCHAR(50) NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority INTEGER CHECK (priority BETWEEN 1 AND 5) DEFAULT 3,
    location GEOMETRY(POINT, 4326),
    estimated_duration INTEGER, -- minutes
    status VARCHAR(20) DEFAULT 'assigned', -- assigned, in_progress, completed, cancelled
    assigned_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_by UUID REFERENCES users(id)
);

-- Events and Timeline
CREATE TABLE stadium_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(50) NOT NULL, -- match_start, goal, halftime, weather_change, emergency
    title VARCHAR(200) NOT NULL,
    description TEXT,
    location GEOMETRY(POINT, 4326),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    impact_radius DECIMAL(10,2), -- meters
    severity INTEGER CHECK (severity BETWEEN 1 AND 5) DEFAULT 3,
    automated BOOLEAN DEFAULT false, -- true if generated by AI
    metadata JSONB, -- flexible event data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Emergencies
CREATE TABLE emergencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    emergency_type emergency_type NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    location GEOMETRY(POINT, 4326) NOT NULL,
    severity INTEGER CHECK (severity BETWEEN 1 AND 5) NOT NULL,
    status VARCHAR(20) DEFAULT 'active', -- active, resolved, escalated
    predicted_impact JSONB, -- AI predictions about the emergency impact
    response_plan TEXT,
    assigned_teams UUID[],
    reported_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE,
    reported_by UUID REFERENCES users(id),
    automated BOOLEAN DEFAULT false
);

-- Crowd Analytics
CREATE TABLE crowd_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID REFERENCES stadium_zones(id),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fan_count INTEGER NOT NULL,
    density DECIMAL(5,2), -- people per square meter
    average_emotion fan_emotion,
    average_stress_level INTEGER,
    average_excitement INTEGER,
    queue_lengths JSONB, -- facility_id -> queue_length mapping
    wait_times JSONB, -- facility_id -> wait_time mapping
    predictions JSONB, -- next 30 minutes predictions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Transport and Traffic
CREATE TABLE transport_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transport_type transport_mode NOT NULL,
    route_name VARCHAR(100) NOT NULL,
    current_capacity INTEGER,
    max_capacity INTEGER,
    delays_minutes INTEGER DEFAULT 0,
    operational_status VARCHAR(20) DEFAULT 'normal', -- normal, delayed, disrupted, closed
    location GEOMETRY(POINT, 4326),
    next_arrival TIMESTAMP WITH TIME ZONE,
    predictions JSONB, -- capacity and timing predictions
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Weather Data
CREATE TABLE weather_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    temperature DECIMAL(4,1), -- Celsius
    humidity INTEGER CHECK (humidity BETWEEN 0 AND 100),
    wind_speed DECIMAL(4,1), -- km/h
    wind_direction INTEGER CHECK (wind_direction BETWEEN 0 AND 360),
    precipitation DECIMAL(5,2), -- mm
    visibility DECIMAL(5,1), -- km
    weather_conditions TEXT, -- clear, cloudy, rainy, stormy
    air_quality_index INTEGER,
    predicted_changes JSONB -- next few hours predictions
);

-- AI Insights and Recommendations
CREATE TABLE ai_insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    insight_type VARCHAR(50) NOT NULL, -- prediction, recommendation, alert, analysis
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0.00 AND 1.00),
    priority INTEGER CHECK (priority BETWEEN 1 AND 5) DEFAULT 3,
    affected_zones UUID[],
    affected_fans UUID[],
    recommended_actions JSONB,
    data_sources TEXT[], -- which data was used to generate this insight
    generated_by VARCHAR(100), -- which AI agent generated this
    valid_until TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active', -- active, implemented, dismissed, expired
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Simulation States (for What-If scenarios)
CREATE TABLE simulation_scenarios (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scenario_name VARCHAR(100) NOT NULL,
    description TEXT,
    scenario_type VARCHAR(50) NOT NULL, -- weather_change, gate_closure, emergency, vip_arrival
    parameters JSONB NOT NULL, -- scenario-specific parameters
    predicted_outcomes JSONB, -- AI predictions for this scenario
    actual_outcomes JSONB, -- if scenario was actually implemented
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true
);

-- System Configuration
CREATE TABLE system_config (
    key VARCHAR(100) PRIMARY KEY,
    value JSONB NOT NULL,
    description TEXT,
    updated_by UUID REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance Metrics
CREATE TABLE performance_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(10,4) NOT NULL,
    unit VARCHAR(20),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    context JSONB -- additional context about the metric
);

-- Indexes for Performance
CREATE INDEX idx_digital_fans_location ON digital_fans USING GIST (current_location);
CREATE INDEX idx_digital_fans_updated_at ON digital_fans (updated_at);
CREATE INDEX idx_digital_fans_active ON digital_fans (is_active) WHERE is_active = true;
CREATE INDEX idx_fan_movements_fan_id_timestamp ON fan_movements (fan_id, timestamp DESC);
CREATE INDEX idx_fan_movements_location ON fan_movements USING GIST (location);
CREATE INDEX idx_fan_predictions_fan_id ON fan_predictions (fan_id);
CREATE INDEX idx_fan_predictions_type_time ON fan_predictions (prediction_type, predicted_time);
CREATE INDEX idx_volunteers_location ON volunteers USING GIST (current_location);
CREATE INDEX idx_volunteers_availability ON volunteers (availability_status) WHERE availability_status = 'available';
CREATE INDEX idx_stadium_events_timestamp ON stadium_events (timestamp DESC);
CREATE INDEX idx_emergencies_status ON emergencies (status) WHERE status = 'active';
CREATE INDEX idx_crowd_analytics_zone_time ON crowd_analytics (zone_id, timestamp DESC);
CREATE INDEX idx_ai_insights_status ON ai_insights (status) WHERE status = 'active';
CREATE INDEX idx_ai_insights_priority ON ai_insights (priority DESC);

-- Functions for common operations
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_digital_fans_updated_at BEFORE UPDATE ON digital_fans FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_volunteers_updated_at BEFORE UPDATE ON volunteers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW active_digital_fans AS
SELECT * FROM digital_fans WHERE is_active = true;

CREATE VIEW current_crowd_density AS
SELECT 
    z.name as zone_name,
    z.id as zone_id,
    COUNT(f.id) as fan_count,
    COALESCE(z.capacity, 0) as capacity,
    CASE 
        WHEN z.capacity > 0 THEN (COUNT(f.id)::DECIMAL / z.capacity) * 100 
        ELSE 0 
    END as occupancy_percentage
FROM stadium_zones z
LEFT JOIN digital_fans f ON ST_Contains(z.coordinates, f.current_location) AND f.is_active = true
GROUP BY z.id, z.name, z.capacity;

CREATE VIEW volunteer_workload AS
SELECT 
    v.id,
    v.name,
    v.availability_status,
    COUNT(vt.id) FILTER (WHERE vt.status IN ('assigned', 'in_progress')) as active_tasks,
    AVG(vt.priority) FILTER (WHERE vt.status IN ('assigned', 'in_progress')) as avg_priority
FROM volunteers v
LEFT JOIN volunteer_tasks vt ON v.id = vt.volunteer_id
WHERE v.is_active = true
GROUP BY v.id, v.name, v.availability_status;

-- Comments
COMMENT ON TABLE digital_fans IS 'Core table storing AI Digital Twins for each stadium visitor';
COMMENT ON TABLE fan_predictions IS 'AI-generated predictions for fan behavior and movements';
COMMENT ON TABLE ai_insights IS 'AI-generated insights, recommendations, and alerts for stadium operations';
COMMENT ON TABLE simulation_scenarios IS 'What-if scenarios and their predicted outcomes';
COMMENT ON COLUMN digital_fans.risk_score IS 'Overall risk score (0-100) combining medical, safety, and behavioral factors';
COMMENT ON COLUMN fan_predictions.confidence_score IS 'AI confidence in prediction accuracy (0.0-1.0)';