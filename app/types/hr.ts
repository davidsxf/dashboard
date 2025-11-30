// 员工相关类型
export interface Employee {
  id: number;
  employee_id: string;
  name: string;
  gender: boolean;
  department_id: number;
  department_name: string;
  team_id?: number;
  team_name?: string;
  nation?: string;
  household_register?: string;
  id_card_number: string;
  birthday?: string;
  native_place?: string;
  birth_place?: string;
  political_status: string;
  party_join_date?: string;
  democratic_party: boolean;
  democratic_party_join_date?: string;
  current_position?: string;
  position_appointment_date?: string;
  position_level?: string;
  professional_title?: string;
  title_appointment_date?: string;
  technical_position?: string;
  technical_position_start_date?: string;
  special_appointment?: string;
  special_appointment_start_date?: string;
  full_time_school?: string;
  full_time_major?: string;
  full_time_education?: string;
  full_time_degree: string;
  full_time_graduation_date?: string;
  in_service_school?: string;
  in_service_major?: string;
  in_service_education?: string;
  in_service_degree: string;
  highest_education?: string;
  highest_degree: string;
  in_service_graduation_date?: string;
  work_start_date?: string;
  join_institute_date?: string;
  institute_household: boolean;
  office_phone?: string;
  mobile_phone?: string;
  email?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  age?: number;
}

// 部门相关类型
export interface Department {
  id: number;
  name: string;
  parent_department_id?: number;
  parent_department_name?: string;
  leader_id?: number;
  leader_name?: string;
  description?: string;
  created_at: string;
  updated_at: string;
  employee_count: number;
}

// 部门树节点类型
export interface DepartmentTreeNode extends Department {
  children: DepartmentTreeNode[];
}

// 科研团队相关类型
export interface ResearchTeam {
  id: number;
  name: string;
  department_id: number;
  department_name: string;
  leader_id?: number;
  leader_name?: string;
  description?: string;
  created_at: string;
  updated_at: string;
  employee_count: number;
}

// 认证相关类型
export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// 分页相关类型
export interface PaginationQuery {
  page: number;
  page_size: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
