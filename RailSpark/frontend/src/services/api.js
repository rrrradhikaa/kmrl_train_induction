import { useApi } from '../hooks/useApi';

// API service functions for different endpoints
export const useTrainApi = () => {
  const { get, post, put, del } = useApi();

  return {
    // Train operations
    getTrains: (skip = 0, limit = 100) => get(`/trains/?skip=${skip}&limit=${limit}`),
    getTrain: (id) => get(`/trains/${id}`),
    createTrain: (trainData) => post('/trains/', trainData),
    updateTrain: (id, trainData) => put(`/trains/${id}`, trainData),
    deleteTrain: (id) => del(`/trains/${id}`),
    getActiveTrains: () => get('/trains/active'),
    updateTrainMileage: (id, additionalMileage) => 
      patch(`/trains/${id}/mileage`, { additional_mileage: additionalMileage })
  };
};

export const useFitnessApi = () => {
  const { get, post, put, del } = useApi();

  return {
    // Fitness certificate operations
    getFitnessCertificates: () => get('/fitness/'),
    getTrainFitness: (trainId) => get(`/fitness/train/${trainId}`),
    getValidCertificates: (trainId) => get(`/fitness/train/${trainId}/valid`),
    createFitnessCertificate: (certData) => post('/fitness/', certData),
    updateFitnessCertificate: (id, certData) => put(`/fitness/${id}`, certData),
    deleteFitnessCertificate: (id) => del(`/fitness/${id}`),
    checkTrainFitness: (trainId) => get(`/fitness/train/${trainId}/service-check`)
  };
};

export const useJobCardApi = () => {
  const { get, post, put, del } = useApi();

  return {
    // Job card operations
    getJobCards: () => get('/job-cards/'),
    getTrainJobCards: (trainId) => get(`/job-cards/train/${trainId}`),
    getOpenJobCards: (trainId = null) => 
      get(trainId ? `/job-cards/open?train_id=${trainId}` : '/job-cards/open'),
    createJobCard: (jobData) => post('/job-cards/', jobData),
    updateJobCard: (id, jobData) => put(`/job-cards/${id}`, jobData),
    deleteJobCard: (id) => del(`/job-cards/${id}`),
    closeJobCard: (id) => patch(`/job-cards/${id}/close`),
    checkOpenJobs: (trainId) => get(`/job-cards/train/${trainId}/has-open-jobs`)
  };
};

export const useBrandingApi = () => {
  const { get, post, put, del } = useApi();

  return {
    // Branding contract operations
    getBrandingContracts: () => get('/branding/'),
    getTrainContracts: (trainId) => get(`/branding/train/${trainId}`),
    getActiveContracts: (trainId = null) => 
      get(trainId ? `/branding/active?train_id=${trainId}` : '/branding/active'),
    getContractsNeedExposure: () => get('/branding/need-exposure'),
    createBrandingContract: (contractData) => post('/branding/', contractData),
    updateBrandingContract: (id, contractData) => put(`/branding/${id}`, contractData),
    deleteBrandingContract: (id) => del(`/branding/${id}`),
    updateExposureHours: (id, hours) => patch(`/branding/${id}/exposure`, { hours })
  };
};

export const useInductionApi = () => {
  const { get, post, put, del } = useApi();

  return {
    // Induction plan operations
    getInductionPlans: () => get('/induction/'),
    getPlansByDate: (date) => get(`/induction/date/${date}`),
    getTodayPlan: () => get('/induction/today'),
    getServiceTrains: (date) => get(`/induction/service-trains/${date}`),
    createInductionPlan: (planData) => post('/induction/', planData),
    createBulkInductionPlans: (plans) => post('/induction/bulk', plans),
    updateInductionPlan: (id, planData) => put(`/induction/${id}`, planData),
    deleteInductionPlan: (id) => del(`/induction/${id}`),
    approveInductionPlan: (id, approvedBy) => 
      patch(`/induction/${id}/approve`, { approved_by: approvedBy })
  };
};

export const useAiApi = () => {
  const { get, post } = useApi();

  return {
    // AI services
    getTrainEligibility: (trainId = null) => 
      trainId ? get(`/ai/eligibility/${trainId}`) : get('/ai/eligibility'),
    generateInductionPlan: (planDate = null, constraints = null) => 
      post('/ai/generate-plan', { plan_date: planDate, constraints }),
    getFailurePredictions: (trainId = null) => 
      trainId ? get(`/ai/failure-predictions/${trainId}`) : get('/ai/failure-predictions'),
    trainModel: () => post('/ai/train-model'),
    getOptimizationStats: () => get('/ai/optimization-stats')
  };
};

export const useChatbotApi = () => {
  const { post, get } = useApi();

  return {
    sendMessage: (message, userId = null) => 
      post('/chatbot/query', { message, user_id: userId }),
    analyzeScenario: (scenarioType, parameters, userId = null) =>
      post('/chatbot/what-if', { scenario_type: scenarioType, parameters, user_id: userId }),
    getContext: (userId) => get(`/chatbot/context/${userId}`),
    clearContext: (userId) => del(`/chatbot/context/${userId}`),
    getCapabilities: () => get('/chatbot/capabilities')
  };
};

export const useDashboardApi = () => {
  const { get } = useApi();

  return {
    getOverview: () => get('/dashboard/overview'),
    getTrainStatus: () => get('/dashboard/train-status'),
    getMaintenanceAlerts: () => get('/dashboard/maintenance-alerts'),
    getBrandingCompliance: () => get('/dashboard/branding-compliance'),
    getPredictiveAnalytics: () => get('/dashboard/predictive-analytics')
  };
};

// Export all services as a single object for easy importing
export const api = {
  trains: useTrainApi,
  fitness: useFitnessApi,
  jobCards: useJobCardApi,
  branding: useBrandingApi,
  induction: useInductionApi,
  ai: useAiApi,
  chatbot: useChatbotApi,
  dashboard: useDashboardApi
};