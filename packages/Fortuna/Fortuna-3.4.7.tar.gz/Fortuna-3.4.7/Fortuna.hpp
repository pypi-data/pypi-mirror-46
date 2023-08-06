#pragma once
#include <cmath>
#include <random>
#include <vector>
#include <limits>
#include <algorithm>


namespace Fortuna {
    using Integer = long long;
    using Float = double;

    static std::random_device hardware_seed {};
    static std::shuffle_order_engine<std::discard_block_engine<std::mt19937_64, 12, 8>, 256> hurricane{hardware_seed()};

    auto min_int() noexcept -> Integer { return std::numeric_limits<Integer>::lowest(); }
    auto max_int() noexcept -> Integer { return std::numeric_limits<Integer>::max(); }
    auto min_float() noexcept -> Float { return std::numeric_limits<Float>::lowest(); }
    auto max_float() noexcept -> Float { return std::numeric_limits<Float>::max(); }
    auto min_below() noexcept -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::lowest()); }
    auto min_above() noexcept -> Float { return std::nextafter(0.0, std::numeric_limits<Float>::max()); }

    template <typename Number>
    auto smart_clamp(Number target, Number left_limit, Number right_limit) noexcept -> Number {
        return std::clamp(target, std::min(left_limit, right_limit), std::max(right_limit, left_limit));
    }

    template <typename Function, typename Number, typename Size>
    auto analytic_continuation(Function && func, Number number, Size offset) noexcept -> Number {
        if (number > 0) return func(number);
        if (number < 0) return -func(-number) + offset;
        return offset;
    }

    auto generate_canonical() noexcept -> Float {
        return std::generate_canonical<Float, std::numeric_limits<Float>::digits>(hurricane);
    }

    auto random_float(Float left_limit, Float right_limit) noexcept -> Float {
        auto distribution = std::uniform_real_distribution<Float> { left_limit, right_limit };
        return distribution(hurricane);
    }

    auto random_int(Integer left_limit, Integer right_limit) noexcept -> Integer {
        auto distribution = std::uniform_int_distribution<Integer> {
            std::min(left_limit, right_limit),
            std::max(right_limit, left_limit)
        };
        return distribution(hurricane);
    }

    auto random_index(Integer size) noexcept -> Integer {
        if (size > 0) {
            auto distribution = std::uniform_int_distribution<Integer> { 0, size - 1 };
            return distribution(hurricane);
        }
        else return analytic_continuation(random_index, size, -1);
    }

    auto random_below(Integer number) noexcept -> Integer {
        if (number > 0) {
            auto distribution = std::uniform_int_distribution<Integer> { 0, number - 1 };
            return distribution(hurricane);
        }
        else return analytic_continuation(random_below, number, 0);
    }


    /// RNG
    auto bernoulli(Float truth_factor) noexcept -> bool {
        auto distribution = std::bernoulli_distribution {
            smart_clamp(truth_factor, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto binomial(Integer number_of_trials, Float probability) noexcept -> Integer {
        auto distribution = std::binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto negative_binomial(Integer number_of_trials, Float probability) noexcept -> Integer {
        auto distribution = std::negative_binomial_distribution<Integer> {
            std::max(number_of_trials, Integer(1)),
            smart_clamp(probability, 0.0, 1.0)
        };
        return distribution(hurricane);
    }

    auto geometric(Float probability) noexcept -> Integer {
        auto distribution = std::geometric_distribution<Integer> { smart_clamp(probability, 0.0, 1.0) };
        return distribution(hurricane);
    }

    auto poisson(Float mean) noexcept -> Integer {
        auto distribution = std::poisson_distribution<Integer> { mean };
        return distribution(hurricane);
    }

    auto expovariate(Float lambda_rate) noexcept -> Float {
        auto distribution = std::exponential_distribution<Float> { lambda_rate };
        return distribution(hurricane);
    }

    auto gammavariate(Float shape, Float scale) noexcept -> Float {
        auto distribution = std::gamma_distribution<Float> { shape, scale };
        return distribution(hurricane);
    }

    auto weibullvariate(Float shape, Float scale) noexcept -> Float {
        auto distribution = std::weibull_distribution<Float> { shape, scale };
        return distribution(hurricane);
    }

    auto normalvariate(Float mean, Float std_dev) noexcept -> Float {
        auto distribution = std::normal_distribution<Float> { mean, std_dev };
        return distribution(hurricane);
    }

    auto lognormvariate(Float log_mean, Float log_deviation) noexcept -> Float {
        auto distribution = std::lognormal_distribution<Float> { log_mean, log_deviation };
        return distribution(hurricane);
    }

    auto extreme_value(Float location, Float scale) noexcept -> Float {
        auto distribution = std::extreme_value_distribution<Float> { location, scale };
        return distribution(hurricane);
    }

    auto chi_squared(Float degrees_of_freedom) noexcept -> Float {
        auto distribution = std::chi_squared_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return distribution(hurricane);
    }

    auto cauchy(Float location, Float scale) noexcept -> Float {
        auto distribution = std::cauchy_distribution<Float> { location, scale };
        return distribution(hurricane);
    }

    auto fisher_f(Float degrees_of_freedom_1, Float degrees_of_freedom_2) noexcept -> Float {
        auto distribution = std::fisher_f_distribution<Float> {
            std::max(degrees_of_freedom_1, Float(0.0)),
            std::max(degrees_of_freedom_2, Float(0.0))
        };
        return distribution(hurricane);
    }

    auto student_t(Float degrees_of_freedom) noexcept -> Float {
        auto distribution = std::student_t_distribution<Float> { std::max(degrees_of_freedom, Float(0.0)) };
        return distribution(hurricane);
    }

    /// Pyewacket
    auto random_range(Integer start, Integer stop, Integer step) noexcept -> Integer {
        if (start == stop) return start;
        auto const width = Integer { std::abs(start - stop) - 1 };
        if (step > 0) return std::min(start, stop) + step * random_below((width + step) / step);
        if (step < 0) return std::max(start, stop) - step * random_below((width - step) / step);
        return start;
    }

    auto betavariate(Float alpha, Float beta) noexcept -> Float {
        auto const y = Float { gammavariate(alpha, 1.0) };
        if (y == 0) return 0.0;
        return y / (y + gammavariate(beta, 1.0));
    }

    auto paretovariate(Float alpha) noexcept -> Float {
        auto const u = Float { 1.0 - generate_canonical() };
        return 1.0 / std::pow(u, 1.0 / alpha);
    }

    auto vonmisesvariate(Float mu, Float kappa) noexcept -> Float {
        static auto const PI = Float { 4 * std::atan(1) };
        static auto const TAU = Float { 2 * PI };
        if (kappa <= 0.000001) return TAU * generate_canonical();
            auto const s = Float { 0.5 / kappa };
            auto const r = Float { s + std::sqrt(1 + s * s) };
            auto u1 = Float {0};
            auto z = Float {0};
            auto d = Float {0};
            auto u2 = Float {0};
            while (true) {
                u1 = generate_canonical();
                z = std::cos(PI * u1);
                d = z / (r + z);
                u2 = generate_canonical();
                if (u2 < 1.0 - d * d or u2 <= (1.0 -d) * std::exp(d)) break;
            }
        auto const q = Float { 1.0 / r };
        auto const f = Float { (q + z) / (1.0 + q * z) };
        auto const u3 = Float { generate_canonical() };
        if (u3 > 0.5) return std::fmod(mu + std::acos(f), TAU);
        else return std::fmod(mu - std::acos(f), TAU);
    }

    auto triangular(Float low, Float high, Float mode) noexcept -> Float {
        if (high - low == 0) return low;
        auto u = Float { generate_canonical() };
        auto c = Float { (mode - low) / (high - low) };
        if (u > c) {
            u = 1.0 - u;
            c = 1.0 - c;
            auto const temp = low;
            low = high;
            high = temp;
        }
        return low + (high - low) * std::sqrt(u * c);
    }

    /// Fortuna
    auto percent_true(Float truth_factor) noexcept -> bool {
        return random_float(0.0, 100.0) < truth_factor;
    }

    auto d(Integer sides) noexcept -> Integer {
        if (sides > 0) return random_int(1, sides);
        else return analytic_continuation(d, sides, 0);
    }

    auto dice(Integer rolls, Integer sides) noexcept -> Integer {
        if (rolls > 0) {
            auto total = Integer {0};
            for (auto i {0}; i < rolls; ++i)
                total += d(sides);
            return total;
        }
        if (rolls == 0) return 0;
        return -dice(-rolls, sides);
    }

    auto ability_dice(Integer num) noexcept -> Integer {
        auto const n { smart_clamp(num, Integer(3), Integer(9)) };
        if (n == 3) return dice(3, 6);
        std::vector<Integer> theRolls(n);
        std::generate(begin(theRolls), end(theRolls), []() { return d(6); });
        std::partial_sort(begin(theRolls), begin(theRolls) + 3, end(theRolls), std::greater<Integer>());
        return std::reduce(begin(theRolls), begin(theRolls) + 3);
    }

    auto plus_or_minus(Integer number) noexcept -> Integer {
        return random_int(-number, number);
    }

    auto plus_or_minus_linear(Integer number) noexcept -> Integer {
        auto const num { std::abs(number) };
        return dice(2, num + 1) - (num + 2);
    }

    auto plus_or_minus_gauss(Integer number) noexcept -> Integer {
        static auto const PI { 4 * std::atan(1) };
        auto const num { std::abs(number) };
        const Integer result = normalvariate(0.0, num/PI);
        if (result >= -num and result <= num) return result;
        return random_int(-num, num);
    }

    auto fuzzy_clamp(Integer target, Integer upper_bound) noexcept -> Integer {
        if (target >= 0 and target < upper_bound) return target;
        else return random_index(upper_bound);
    }

    /// ZeroCool Methods
    auto front_gauss(Integer number) noexcept -> Integer;
    auto middle_gauss(Integer number) noexcept -> Integer;
    auto back_gauss(Integer number) noexcept -> Integer;
    auto quantum_gauss(Integer number) noexcept -> Integer;
    auto front_poisson(Integer number) noexcept -> Integer;
    auto middle_poisson(Integer number) noexcept -> Integer;
    auto back_poisson(Integer number) noexcept -> Integer;
    auto quantum_poisson(Integer number) noexcept -> Integer;
    auto front_linear(Integer number) noexcept -> Integer;
    auto middle_linear(Integer number) noexcept -> Integer;
    auto back_linear(Integer number) noexcept -> Integer;
    auto quantum_linear(Integer number) noexcept -> Integer;
    auto quantum_monty(Integer number) noexcept -> Integer;


    auto front_gauss(Integer number) noexcept -> Integer {
        if (number > 0) {
            auto const result { Integer(gammavariate(1.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(back_gauss, number, -1);
    }

    auto middle_gauss(Integer number) noexcept -> Integer {
        if (number > 0) {
            auto const result { Integer(normalvariate(number / 2.0, number / 10.0)) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(middle_gauss, number, -1);
    }

    auto back_gauss(Integer number) noexcept -> Integer {
        if (number > 0) {
            return number - front_gauss(number) - 1;
        }
        else return analytic_continuation(front_gauss, number, -1);
    }

    auto quantum_gauss(Integer number) noexcept -> Integer {
        auto const rand_num { d(3) };
        if (rand_num == 1) return front_gauss(number);
        else if (rand_num == 2) return middle_gauss(number);
        else return back_gauss(number);
    }

    auto front_poisson(Integer number) noexcept -> Integer {
        if (number > 0) {
            auto const result { poisson(number / 4.0) };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(back_poisson, number, -1);
    }

    auto back_poisson(Integer number) noexcept -> Integer {
        if (number > 0) {
            auto result { number - front_poisson(number) - 1 };
            return fuzzy_clamp(result, number);
        }
        else return analytic_continuation(front_poisson, number, -1);
    }

    auto middle_poisson(Integer number) noexcept -> Integer {
        if (percent_true(50)) return front_poisson(number);
        else return back_poisson(number);
    }

    auto quantum_poisson(Integer number) noexcept -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return front_poisson(number);
        else if (rand_num == 2) return middle_poisson(number);
        else return back_poisson(number);
    }

    auto front_linear(Integer number) noexcept -> Integer {
        if (number > 0) {
            return triangular(0, number, 0);
        }
        else return analytic_continuation(back_linear, number, -1);
    }

    auto back_linear(Integer number) noexcept -> Integer {
        if (number > 0) {
            return triangular(0, number, number);
        }
        else return analytic_continuation(front_linear, number, -1);
    }

    auto middle_linear(Integer number) noexcept -> Integer {
        if (number > 0) {
            return triangular(0, number, number / 2.0);
        }
        else return analytic_continuation(middle_linear, number, -1);
    }

    auto quantum_linear(Integer number) noexcept -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return front_linear(number);
        else if (rand_num == 2) return middle_linear(number);
        else return back_linear(number);
    }

    auto quantum_monty(Integer number) noexcept -> Integer {
        auto rand_num { d(3) };
        if (rand_num == 1) return quantum_linear(number);
        else if (rand_num == 2) return quantum_gauss(number);
        else return quantum_poisson(number);
    }

    /// Generators
    template<typename Value>
    auto random_value(const std::vector<Value> & vec) noexcept -> Value {
        return vec[random_index(vec.size())];
    }

    template<typename Value>
    auto shuffled_vec(std::vector<Value> vec) noexcept -> std::vector<Value> {
        std::shuffle(begin(vec), end(vec), hurricane);
        return vec;
    }

    template<typename Value>
    auto pop(std::vector<Value> & vec, size_t idx) noexcept -> Value {
        assert(vec.size() > idx);
        const Value result = vec[idx];
        vec.erase(begin(vec) + idx);
        return result;
    }

    template<typename Value>
    auto insert(std::vector<Value> & vec, size_t idx, Value val) noexcept -> void {
        vec.insert(begin(vec) + idx, val);
    }

    /// Classes
    template<typename Value>
    class TruffleShuffle {
        std::vector<Value> data;
        const size_t max_id;
    public:
        TruffleShuffle(std::vector<Value> vec_of_values) : data(vec_of_values), max_id(vec_of_values.size() - 1) {
            assert(not data.empty() && "Empty Vector!");
            std::shuffle(begin(data), end(data), hurricane);
        }
        auto operator()() noexcept -> Value {
            const Value result = data[max_id];
            data.erase(data.begin() + max_id);
            data.insert(data.begin() + front_poisson(max_id), result);
            return result;
        }
    };

    template<typename Value>
    struct QuantumMonty {
        const std::vector<Value> table;
        Value operator()() const noexcept {
            return table[quantum_monty(int(table.size()))];
        }
        Value operator()(const std::string & monty) const noexcept {
            const auto size = int(table.size());
            if (monty == "uniform_flat") return table[random_index(size)];
            if (monty == "front_linear") return table[front_linear(size)];
            if (monty == "middle_linear") return table[middle_linear(size)];
            if (monty == "back_linear") return table[back_linear(size)];
            if (monty == "quantum_linear") return table[quantum_linear(size)];
            if (monty == "front_gauss") return table[front_gauss(size)];
            if (monty == "middle_gauss") return table[middle_gauss(size)];
            if (monty == "back_gauss") return table[back_gauss(size)];
            if (monty == "quantum_gauss") return table[quantum_gauss(size)];
            if (monty == "front_poisson") return table[front_poisson(size)];
            if (monty == "middle_poisson") return table[middle_poisson(size)];
            if (monty == "back_poisson") return table[back_poisson(size)];
            if (monty == "quantum_poisson") return table[quantum_poisson(size)];
            if (monty == "quantum_monty") return table[quantum_monty(size)];
            assert(!"Monty not found");
            return table[quantum_monty(size)];
        }
    };

    template<typename Weight>
    auto cumulative_from_relative(std::vector<Weight> vec) noexcept -> std::vector<Weight> {
        std::partial_sum(vec.begin(), vec.end(), vec.begin());
        return vec;
    }

    template<typename Weight>
    auto relative_from_cum_vec(std::vector<Weight> vec) noexcept -> std::vector<Weight> {
        std::adjacent_difference(vec.begin(), vec.end(), vec.begin());
        return vec;
    }

    template<typename Weight, typename Value>
    struct CumulativeWeightedChoice {
        // Weights must be unique numeric values sorted from low to high.
        // Values can be any value type.
        const std::vector<Weight> weights;
        const std::vector<Value> values;
        auto operator()() const noexcept -> Value {
            const auto max_weight = weights.back();
            const auto raw_weight = random_float(0.0, max_weight);
            const auto valid_weight = std::lower_bound(weights.begin(), weights.end(), raw_weight);
            const auto result_idx = std::distance(weights.begin(), valid_weight);
            return values[result_idx];
        }
    };

} // end namespace
